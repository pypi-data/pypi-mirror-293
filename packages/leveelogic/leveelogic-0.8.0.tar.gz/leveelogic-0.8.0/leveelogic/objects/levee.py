import os
from dotenv import load_dotenv
from typing import List, Tuple, Union, Optional
from shapely.geometry import Polygon, MultiPolygon
from shapely import get_coordinates
from shapely.ops import orient, unary_union
from pathlib import Path
from geolib.geometry.one import Point
from geolib.soils.soil import Soil as GLSoil, ShearStrengthModelTypePhreaticLevel
from geolib.models.dstability.loads import UniformLoad, Consolidation, TreeLoad
from geolib.models.dstability.analysis import (
    PersistableBishopBruteForceSettings,
    PersistableSpencerGeneticSettings,
    PersistableUpliftVanParticleSwarmSettings,
    DStabilityBishopBruteForceAnalysisMethod,
    DStabilitySearchGrid,
    DStabilitySlipPlaneConstraints,
)
from geolib.models.dstability.internal import AnalysisTypeEnum
from pydantic import PrivateAttr
from enum import IntEnum

from ..models.datamodel import DataModel
from .soilprofile import SoilProfile
from .soil import Soil
from .soilpolygon import SoilPolygon
from ..external.dgeolib import DStabilityModel
from .crosssection import Crosssection
from .soillayer import SoilLayer
from ..helpers import polyline_polyline_intersections, is_on_line, is_part_of_line
from ..settings import (
    DEFAULT_LOAD_CONSOLIDATION,
    DEFAULT_LOAD_SPREAD,
    DEFAULT_TREE_WIDTH_ROOTZONE,
    DEFAULT_TREE_DEPTH_EXCAVATION,
    MIN_GEOM_SIZE,
)


class TreeLoadMode(IntEnum):
    LOAD = 1  # treat the tree as a load that causes a load on the soil
    EXCAVATION = 2  # treat the tree as an excavation


class TrafficLoad(DataModel):
    left: float
    width: float
    magnitude: float
    spread: float
    consolidation: float


class Tree(DataModel):
    x: float
    height: float
    wind_force: float
    width: float
    depth: float
    spread: float
    mode: TreeLoadMode = TreeLoadMode.EXCAVATION


class AnalysisType(IntEnum):
    UNDEFINED = 0
    BISHOP_BRUTE_FORCE = 1
    UPLIFT_VAN_PARTICLE_SWARM = 2
    SPENCER_GENETIC = 3


class Levee(DataModel):
    soilpolygons: List[SoilPolygon] = []
    soils: List[Soil] = []
    _x_reference_line: float = None
    _ditch_points: List[Tuple[float, float]] = []
    _phreatic_line: List[Tuple[float, float]] = []
    _traffic_load: TrafficLoad = None
    _tree: Tree = None
    _bbf: PersistableBishopBruteForceSettings = None
    _spencer: PersistableSpencerGeneticSettings = None
    _upliftvan: PersistableUpliftVanParticleSwarmSettings = None

    class Config:
        underscore_attrs_are_private = True

    @property
    def phreatic_line(self) -> List[Tuple[float, float]]:
        return self._phreatic_line

    @classmethod
    def from_stix(
        cls,
        stix_file: str,
        x_reference_line: float = None,
        scenario_index: int = 0,
        stage_index: int = 0,
        calculation_index: int = 0,
    ):
        dm = DStabilityModel.from_stix(stix_file)

        result = Levee()

        if x_reference_line is not None:
            result.set_x_reference_line(x_reference_line)

        cs = dm.get_calculation_settings(
            scenario_index=scenario_index, calculation_index=calculation_index
        )
        if cs is not None:
            if cs.AnalysisType == AnalysisTypeEnum.BISHOP_BRUTE_FORCE:
                result._bbf = cs.BishopBruteForce
            elif cs.AnalysisType == AnalysisTypeEnum.SPENCER_GENETIC:
                result._spencer = cs.SpencerGenetic
            elif cs.AnalysisType == AnalysisTypeEnum.UPLIFT_VAN_PARTICLE_SWARM:
                result._upliftvan = cs.UpliftVanParticleSwarm

        layers = dm._get_geometry(scenario_index, stage_index).Layers

        # get the soil colors based on the Id
        soilcolors = {
            sv.SoilId: sv.Color[:1] + sv.Color[3:]  # remove the alpha part
            for sv in dm.datastructure.soilvisualizations.SoilVisualizations
        }

        # add all the soils and get the soil codes based on the Id
        soil_codes = {}
        for soil in dm.soils.Soils:
            c = 0.0
            phi = 0.0
            if soil.MohrCoulombAdvancedShearStrengthModel.Cohesion is not None:
                c = soil.MohrCoulombAdvancedShearStrengthModel.Cohesion
            elif soil.MohrCoulombClassicShearStrengthModel.Cohesion is not None:
                c = soil.MohrCoulombClassicShearStrengthModel.Cohesion
            if soil.MohrCoulombAdvancedShearStrengthModel.FrictionAngle is not None:
                phi = soil.MohrCoulombAdvancedShearStrengthModel.FrictionAngle
            elif soil.MohrCoulombClassicShearStrengthModel.FrictionAngle is not None:
                phi = soil.MohrCoulombClassicShearStrengthModel.FrictionAngle

            result.soils.append(
                Soil(
                    code=soil.Code,
                    yd=soil.VolumetricWeightAbovePhreaticLevel,
                    ys=soil.VolumetricWeightBelowPhreaticLevel,
                    c=c,
                    phi=phi,
                    color=soilcolors[soil.Id],
                )
            )
            soil_codes[soil.Id] = soil.Code

        # get the connection between the layer Id and the soil Id
        soillayer_id_dict = {}
        for sl in dm.datastructure._get_soil_layers(
            scenario_index, stage_index
        ).SoilLayers:
            soillayer_id_dict[sl.LayerId] = sl.SoilId

        # finally create the collection of soilpolygons
        for layer in layers:
            result.soilpolygons.append(
                SoilPolygon(
                    soilcode=soil_codes[soillayer_id_dict[layer.Id]],
                    points=[(float(p.X), float(p.Z)) for p in layer.Points],
                )
            )

        # get the phreatic line if available
        try:
            result.add_phreatic_line(dm.phreatic_line(scenario_index, stage_index))
        except:
            pass

        return result

    @classmethod
    def from_soilprofiles(
        cls,
        profile_waterside: SoilProfile,
        profile_landside: SoilProfile,
        crosssection: Crosssection,
        x_landside: float,
        soils: List[Soil],
        fill_soilcode: str,
        x_reference_line: Optional[float] = None,
    ):
        result = Levee()
        if x_reference_line is not None:
            result.set_x_reference_line(x_reference_line)
        top = max(profile_landside.top, profile_waterside.top)
        top = max(top, crosssection.top)
        bottom = min(profile_landside.bottom, profile_waterside.bottom)
        bottom = min(bottom, crosssection.bottom)

        result.soils = soils

        if profile_landside.top < top:
            profile_landside.soillayers.insert(
                0,
                SoilLayer(
                    top=top,
                    bottom=profile_landside.soillayers[0].top,
                    soilcode=fill_soilcode,
                ),
            )
            profile_landside.merge()

        if profile_waterside.top < top:
            profile_waterside.soillayers.insert(
                0,
                SoilLayer(
                    top=top,
                    bottom=profile_waterside.soillayers[0].top,
                    soilcode=fill_soilcode,
                ),
            )
            profile_waterside.merge()

        profile_landside.set_bottom(bottom)
        profile_waterside.set_bottom(bottom)

        result.soilpolygons = profile_landside.to_soilpolygons(
            left=crosssection.left, right=x_landside
        )
        result.soilpolygons += profile_waterside.to_soilpolygons(
            left=x_landside, right=crosssection.right
        )

        cut_line = [p for p in crosssection.points]
        cut_line.append((cut_line[-1][0], top + 1.0))
        cut_line.append((cut_line[0][0], top + 1.0))

        result._cut(cut_line)

        return result

    @property
    def ditch_points(self) -> List[Tuple[float, float]]:
        return self._ditch_points

    @property
    def analysis_type(self) -> AnalysisType:
        if self._bbf is not None:
            return AnalysisType.BISHOP_BRUTE_FORCE
        elif self._spencer is not None:
            return AnalysisType.SPENCER_GENETIC
        elif self._upliftvan is not None:
            return AnalysisType.UPLIFT_VAN_PARTICLE_SWARM

        return AnalysisType.UNDEFINED

    @property
    def surface(self) -> List[Tuple[float, float]]:
        """Get the surface line of the geometry from left to right

        Returns:
            List[Tuple[float, float]]: The points that form the surface of the levee
        """
        boundary = self.as_one_polygon()
        boundary = [
            (round(p[0], 3), round(p[1], 3))
            for p in list(zip(*boundary.exterior.coords.xy))[:-1]
        ]
        # get the leftmost point
        left = min([p[0] for p in boundary])
        topleft_point = sorted(
            [p for p in boundary if p[0] == left], key=lambda x: x[1]
        )[-1]

        # get the rightmost points
        right = max([p[0] for p in boundary])
        rightmost_point = sorted(
            [p for p in boundary if p[0] == right], key=lambda x: x[1]
        )[-1]

        # get the index of leftmost point
        idx_left = boundary.index(topleft_point)
        surface = boundary[idx_left:] + boundary[:idx_left]

        # get the index of the rightmost point
        idx_right = surface.index(rightmost_point)
        surface = surface[: idx_right + 1]
        return surface

    @property
    def bottom_surface(self) -> List[Tuple[float, float]]:
        """Get the bottom line of the geometry from left to right

        Returns:
            List[Tuple[float, float]]: The point that from the bottom of the levee
        """
        boundary = self.as_one_polygon()
        boundary = [
            (round(p[0], 3), round(p[1], 3))
            for p in list(zip(*boundary.exterior.coords.xy))[:-1]
        ]
        # get the leftmost point
        left = min([p[0] for p in boundary])
        bottomleft_point = sorted(
            [p for p in boundary if p[0] == left], key=lambda x: x[1]
        )[0]

        # get the rightmost points
        right = max([p[0] for p in boundary])
        rightmost_point = sorted(
            [p for p in boundary if p[0] == right], key=lambda x: x[1]
        )[0]

        # get the index of leftmost point
        idx_left = boundary.index(bottomleft_point)

        # get the index of the rightmost point
        idx_right = boundary.index(rightmost_point)
        return boundary[idx_right : idx_left + 1][::-1]

    @property
    def all_points(self) -> List[Tuple[float, float]]:
        points = []
        for pg in self.soilpolygons:
            points += pg.points
        return points

    @property
    def left(self) -> float:
        return min([p[0] for p in self.all_points])

    @property
    def right(self) -> float:
        return max([p[0] for p in self.all_points])

    @property
    def top(self) -> float:
        return max([p[1] for p in self.all_points])

    @property
    def bottom(self) -> float:
        return min([p[1] for p in self.all_points])

    def get_soil_by_code(
        self, code: str, case_sensitive: bool = False
    ) -> Optional[Soil]:
        for soil in self.soils:
            if case_sensitive:
                if soil.code == code:
                    return soil
            else:
                if soil.code.lower() == code.lower():
                    return soil
        return None

    @property
    def has_ditch(self) -> bool:
        return len(self._ditch_points) > 0

    @property
    def has_traffic_load(self) -> bool:
        return self._traffic_load is not None

    @property
    def x_reference_line(self) -> Optional[float]:
        return self._x_reference_line

    def set_x_reference_line(self, x: float):
        self._x_reference_line = x

    def as_one_polygon(self) -> Polygon:
        polygons = []
        for pg in self.soilpolygons:
            polygons.append(Polygon(pg.points))

        return orient(unary_union(polygons), sign=-1)

    def _cut(self, cut_line: List[Tuple[float, float]]):
        """Cut a piece defined by the given line out of the geometry

        Args:
            cut_line (List[Tuple[float, float]]): The line that defines the bottom of the part to be cut out (should increase in x coordinates)

        Raises:
            ValueError: Raises ValueError is the input or output is incorrect
        """
        # add the begin and end point to the cut line to form a polygon
        points = [p for p in cut_line]
        points.insert(0, (cut_line[0][0], self.top + 1.0))
        points.append((cut_line[-1][0], self.top + 1.0))

        pg_extract = Polygon(points)
        new_soilpolygons = []
        for spg in self.soilpolygons:
            pg = spg.to_shapely()

            pgs = pg.difference(pg_extract)

            if type(pgs) == MultiPolygon:
                geoms = pgs.geoms
            elif type(pgs) == Polygon:
                geoms = [pgs]
            else:
                raise ValueError(f"Unhandled polygon difference type '{type(pgs)}'")

            for geom in geoms:
                if geom.is_empty:
                    continue
                points = get_coordinates(geom).tolist()
                new_soilpolygons.append(
                    SoilPolygon(points=points, soilcode=spg.soilcode)
                )

        self.soilpolygons = new_soilpolygons

    def _fill(
        self,
        fill_line: List[Tuple[float, float]],
        soilcode: str,
    ):
        if polyline_polyline_intersections(self.bottom_surface, fill_line):
            raise ValueError(
                "The fill line intersects with the bottom of the geometry which will cause an invalid result"
            )

        x_start = fill_line[0][0]
        x_end = fill_line[-1][0]
        surface_points = [p for p in self.surface if p[0] >= x_start and p[0] <= x_end]
        zmin = min([p[1] for p in surface_points + fill_line]) - 1.0
        fill_line.append((x_end, zmin))
        fill_line.append((x_start, zmin))

        pg_fill = Polygon(fill_line)
        pg_current = self.as_one_polygon()

        pgs = pg_fill.difference(pg_current)
        geoms = []
        if type(pgs) == MultiPolygon:
            geoms = pgs.geoms
        elif type(pgs) == Polygon:
            geoms = [pgs]
        else:
            raise ValueError(f"Unhandled polygon difference type '{type(pgs)}'")

        for geom in geoms:
            if geom.is_empty or geom.area < MIN_GEOM_SIZE:
                continue
            points = get_coordinates(geom).tolist()
            self.soilpolygons.append(SoilPolygon(points=points, soilcode=soilcode))

    def _fix_missing_points(self):
        # check if we have points that should be on other polygons as well
        for point in self.all_points:
            for i, spg in enumerate(self.soilpolygons):
                for j, line in enumerate(spg.lines):
                    p1 = line[0]
                    p2 = line[1]
                    if is_on_line(p1, p2, point) and not is_part_of_line(p1, p2, point):
                        if j == len(spg.points) - 1:
                            self.soilpolygons[i].points.insert(0, point)
                        else:
                            self.soilpolygons[i].points.insert(j + 1, point)

    def _surface_points_between(
        self, x_start: float, x_end: float
    ) -> List[Tuple[float, float]]:
        return [p for p in self.surface if x_start < p[0] and p[0] < x_end]

    def add_phreatic_line(self, points: List[Tuple[float, float]]):
        self._phreatic_line = points

    def add_traffic_load(
        self,
        left: float,
        width: float,
        magnitude: float,
        spread: float = DEFAULT_LOAD_SPREAD,
        consolidation: float = DEFAULT_LOAD_CONSOLIDATION,
    ):
        self._traffic_load = TrafficLoad(
            left=left,
            width=width,
            magnitude=magnitude,
            spread=spread,
            consolidation=consolidation,
        )

    def add_berm(
        self,
        x: float,
        z: float,
        berm_soilcode: str,
        slope_top: float = 10.0,
        slope_side: float = 3.0,
        add_ditch: bool = False,
        ditch_offset: float = 0.0,
        ditch_slope: float = 2.0,
        ditch_bottom_level: float = 0.0,
        ditch_bottom_width: float = 1.0,
    ):
        if self._x_reference_line is None:
            raise ValueError(
                "If you want to use the add_berm functionality you need to assign a value to the x_reference_line parameter of this levee"
            )
        slope_points_top = [(self.left, z + (x - self.left) / slope_top), (x, z)]
        slope_line_side = [(x, z), (self.right, z - (self.right - x) / slope_side)]

        intersections_top = polyline_polyline_intersections(
            slope_points_top, self.surface
        )
        # remove those before the reference line point
        intersections_top = [
            p for p in intersections_top if p[0] > self._x_reference_line
        ]
        if len(intersections_top) == 0:
            raise ValueError(
                "No intersection with the surface found for the top line of the berm, check the slope and start point of the berm"
            )

        intersections_side = polyline_polyline_intersections(
            slope_line_side, self.surface
        )
        if len(intersections_side) == 0:
            raise ValueError(
                "No intersections with the surface found for the side line of the berm, check the slope and start point"
            )

        pA = intersections_top[0]
        pB = (x, z)
        pC = intersections_side[-1]

        intersections = polyline_polyline_intersections([pA, pB, pC], self.surface)
        # if we have an uneven number of intersections (but more than 1) remove the last one
        if len(intersections) < 2:
            raise ValueError(
                "No intersections with the surface found for the berm, check the slope and start point"
            )

        if len(intersections) % 2 != 0:
            intersections = intersections[:-1]

        for i in range(0, len(intersections), 2):
            # get the left and right point of the berm
            p1 = intersections[i]
            p2 = intersections[i + 1]

            # check if we need to add the knikpunt of the berm
            if p1[0] < pB[0] and pB[0] < p2[0]:
                points = [p1, pB, p2]
            else:
                points = [p1, p2]

            # now follow the surface back to p1
            points += self._surface_points_between(p1[0], p2[0])[::-1]

            self.soilpolygons.append(SoilPolygon(soilcode=berm_soilcode, points=points))

        # replace ditch next to berm
        if add_ditch:
            self.add_ditch(
                x_start=pC[0] + ditch_offset,
                slope=ditch_slope,
                bottom_level=ditch_bottom_level,
                bottom_width=ditch_bottom_width,
            )

        self._fix_missing_points()

    def add_bbf_constraints(
        self, min_slipplane_length: float = None, min_slipplane_depth: float = None
    ):
        if self._bbf is not None:
            self._bbf.SlipPlaneConstraints.IsSizeConstraintsEnabled = True
            if min_slipplane_depth is not None:
                self._bbf.SlipPlaneConstraints.MinimumSlipPlaneDepth = (
                    min_slipplane_depth
                )
            if min_slipplane_length is not None:
                self._bbf.SlipPlaneConstraints.MinimumSlipPlaneLength = (
                    min_slipplane_length
                )
        else:
            raise ValueError(
                "Trying to set constraints to the BishopBruteForce method but no BBF settings found."
            )

    def fill_ditch(self, soilcode: str):
        self._fill([self._ditch_points[0], self._ditch_points[-1]], soilcode=soilcode)

    def add_ditch(
        self, x_start: float, slope: float, bottom_level: float, bottom_width: float
    ):
        # topleft point
        x1 = x_start
        z1 = self.z_at(x_start)
        # bottomleft point
        z2 = bottom_level
        x2 = x1 + (z1 - bottom_level) * slope
        # bottomright point
        x3 = x2 + bottom_width
        z3 = z2

        self._ditch_points = [(x1, z1), (x2, z2), (x3, z3)]

        slope_line = (x3, z3), (x3 + 1e3, z3 + 1e3 / slope)
        intersections = polyline_polyline_intersections(self.surface, slope_line)

        if len(intersections) > 0:
            self._ditch_points.append(intersections[0])

        # cut out the ditch
        self._cut(self._ditch_points)

    def z_at(self, x: float, top_only: bool = True) -> Union[float, List[float]]:
        line = [(x, self.top + 1.0), (x, self.bottom - 1.0)]

        intersections = []
        for pg in self.soilpolygons:
            intersections += polyline_polyline_intersections(line, pg.points)

        intersections = sorted([p[1] for p in list(set(intersections))])[::-1]

        if top_only:
            return intersections[0]
        else:
            return intersections

    def phreatic_level_at(self, x: float) -> Optional[float]:
        for i in range(1, len(self._phreatic_line)):
            x1, z1 = self._phreatic_line[i - 1]
            x2, z2 = self._phreatic_line[i]
            if x1 <= x and x <= x2:
                return z1 + (x - x1) / (x2 - x1) * (z2 - z1)

        return None

    def get_surface_intersections(
        self, points: List[Tuple[float, float]]
    ) -> List[Tuple[float, float]]:
        return polyline_polyline_intersections(points, self.surface)

    def add_tree_as_excavation(
        self,
        x: float,
        width: float = DEFAULT_TREE_WIDTH_ROOTZONE,
        depth: float = DEFAULT_TREE_DEPTH_EXCAVATION,
    ):
        self._tree = Tree(
            x=x,
            height=0.0,
            wind_force=0.0,
            width=width,
            depth=depth,
            spread=0.0,
            mode=TreeLoadMode.EXCAVATION,
        )

    def add_tree_as_load(
        self,
        x: float,
        height: float,
        wind_force: float,
        width: float = DEFAULT_TREE_WIDTH_ROOTZONE,
        spread: float = DEFAULT_LOAD_SPREAD,
    ):
        self._tree = Tree(
            x=x,
            height=height,
            wind_force=wind_force,
            width=width,
            depth=0.0,
            spread=spread,
            mode=TreeLoadMode.LOAD,
        )

    def add_toplayer(
        self,
        x_start: float,
        x_end: float,
        height: float,
        soilcode: str,
    ):
        if x_end - x_start <= 0:
            raise ValueError(
                f"X start ({x_start}) cannot be greater than X end ({x_end})"
            )

        p_start = (x_start, self.z_at(x_start))
        p_end = (x_end, self.z_at(x_end))
        cut_line = [(p_start[0], p_start[1] - height)] + [
            (p[0], p[1] - height)
            for p in self.surface
            if p[0] > x_start and p[0] < x_end
        ]
        if cut_line[-1][0] != x_end:
            cut_line += [(p_end[0], p_end[1] - height)]

        fill_line = (
            [p_start]
            + [p for p in self.surface if x_start < p[0] and p[0] < x_end]
            + [p_end]
        )
        self._cut(cut_line)
        self._fill(fill_line, soilcode=soilcode)

    def to_stix(self, filename: str):
        """Generate a stix file from the input

        Args:
            filename (str): The file to save the stix to

        Raises:
            ValueError: Raises an exception if there is an error with the geometry
        """
        dm = DStabilityModel()
        default_soilcodes = [s.Code for s in dm.soils.Soils]

        # add the soils
        # and keep track of the consolidations
        consolidations_dict = {}

        soilcodes_in_layers = [spg.soilcode for spg in self.soilpolygons]
        for soil in self.soils:
            # only add soils that are used in the layers
            if not soil.code in soilcodes_in_layers:
                continue

            # TODO, should preferably overwrite the parameters with the new ones
            # for now defaulting to original parameters
            if soil.code in default_soilcodes:
                if soil.code in [
                    "P_Rk_k&s",
                    "H_Rk_k_deep",
                    "H_Rk_k_shallow",
                    "Dilatent clay",
                    "Embankment dry",
                    "H_Aa_ht_new",
                    "H_Aa_ht_old",
                    "H_Rk_ko",
                    "H_vbv_v",
                    "H_vhv_v",
                ]:
                    consolidations_dict[soil.code] = DEFAULT_LOAD_CONSOLIDATION
                elif soil.code in ["Sand", "H_Ro_z&k"]:
                    consolidations_dict[soil.code] = 100.0
                else:
                    raise ValueError(
                        f"Unknown default soilcode '{soil.code}' found, you need to assign this code to the corresponding consolidation factor."
                    )
                continue

            gl_soil = GLSoil()
            gl_soil.name = soil.code
            gl_soil.code = soil.code
            gl_soil.soil_weight_parameters.saturated_weight.mean = soil.ys
            gl_soil.soil_weight_parameters.unsaturated_weight.mean = soil.yd
            gl_soil.mohr_coulomb_parameters.cohesion.mean = soil.c
            gl_soil.mohr_coulomb_parameters.friction_angle.mean = soil.phi
            gl_soil.mohr_coulomb_parameters.dilatancy_angle = soil.phi
            gl_soil.shear_strength_model_above_phreatic_level = (
                ShearStrengthModelTypePhreaticLevel.MOHR_COULOMB
            )
            gl_soil.shear_strength_model_below_phreatic_level = (
                ShearStrengthModelTypePhreaticLevel.MOHR_COULOMB
            )
            id = dm.add_soil(gl_soil)
            if soil.c > 0.1:
                consolidations_dict[soil.code] = DEFAULT_LOAD_CONSOLIDATION
            else:
                consolidations_dict[soil.code] = 100.0

        # if we have a tree that changes the geometry we need to do it before adding the layers
        if self._tree is not None and self._tree.mode == TreeLoadMode.EXCAVATION:
            x1 = self._tree.x - 0.5 * self._tree.width
            x2 = self._tree.x + 0.5 * self._tree.width
            z1 = self.z_at(x1)
            z2 = self.z_at(x2)

            exc_line = [(x1, z1), (x1, z1 - self._tree.depth)]
            exc_line += [
                (p[0], p[1] - self._tree.depth)
                for p in self.surface
                if p[0] > x1 and p[0] < x2
            ]
            exc_line += [(x2, z2 - self._tree.depth), (x2, z2)]
            self._cut(cut_line=exc_line)

        # add the layers
        layer_consolidation_dict = {}
        layer_ids = []
        for i, spg in enumerate(self.soilpolygons):
            points = [Point(x=p[0], z=p[1]) for p in spg.points]
            try:
                layer_id = dm.add_layer(points, soil_code=spg.soilcode, label=f"L{i+1}")
            except Exception as e:
                raise ValueError(f"Error adding layer with point = {spg.points}")
            layer_ids.append(layer_id)
            layer_consolidation_dict[layer_id] = consolidations_dict[spg.soilcode]

        # add phreatic line
        if len(self._phreatic_line) > 0:
            dm.add_head_line(
                points=[Point(x=p[0], z=p[1]) for p in self._phreatic_line],
                label="PL1",
                is_phreatic_line=True,
            )

        # add the load
        if self._traffic_load is not None:
            # adjust to the consolidation degree given for the traffic load
            for k, v in layer_consolidation_dict.items():
                if v != 100.0:
                    layer_consolidation_dict[k] = self._traffic_load.consolidation
            dm.add_load(
                UniformLoad(
                    label="Traffic",
                    start=self._traffic_load.left,
                    end=self._traffic_load.left + self._traffic_load.width,
                    magnitude=self._traffic_load.magnitude,
                    angle_of_distribution=self._traffic_load.spread,
                ),
                consolidations=[
                    Consolidation(
                        degree=layer_consolidation_dict[layer_id], layer_id=layer_id
                    )
                    for layer_id in layer_ids
                ],
            )

        # if we add a tree as a load we need the layer ids for the cons degrees so this needs to
        # happen after adding the layers
        if self._tree is not None and self._tree.mode == TreeLoadMode.LOAD:
            z = self.z_at(self._tree.x) + self._tree.height
            dm.add_load(
                TreeLoad(
                    tree_top_location=Point(x=self._tree.x, z=z),
                    wind_force=self._tree.wind_force,
                    width_of_root_zone=self._tree.width,
                    angle_of_distribution=self._tree.spread,
                ),
                consolidations=[
                    Consolidation(
                        degree=layer_consolidation_dict[layer_id], layer_id=layer_id
                    )
                    for layer_id in layer_ids
                ],
            )

        # do we have BBF settings?
        if self._bbf is not None:
            search_grid = self._bbf.SearchGrid
            slip_plane_constraints = self._bbf.SlipPlaneConstraints
            tangent_lines = self._bbf.TangentLines

            if search_grid is not None and tangent_lines is not None:
                if slip_plane_constraints is None:
                    dm.set_model(
                        DStabilityBishopBruteForceAnalysisMethod(
                            search_grid=DStabilitySearchGrid(
                                bottom_left=Point(
                                    x=search_grid.BottomLeft.X,
                                    z=search_grid.BottomLeft.Z,
                                ),
                                number_of_points_in_x=search_grid.NumberOfPointsInX,
                                number_of_points_in_z=search_grid.NumberOfPointsInZ,
                                space=search_grid.Space,
                            ),
                            bottom_tangent_line_z=tangent_lines.BottomTangentLineZ,
                            number_of_tangent_lines=tangent_lines.NumberOfTangentLines,
                            space_tangent_lines=tangent_lines.Space,
                        )
                    )
                else:
                    dm.set_model(
                        DStabilityBishopBruteForceAnalysisMethod(
                            search_grid=DStabilitySearchGrid(
                                bottom_left=Point(
                                    x=search_grid.BottomLeft.X,
                                    z=search_grid.BottomLeft.Z,
                                ),
                                number_of_points_in_x=search_grid.NumberOfPointsInX,
                                number_of_points_in_z=search_grid.NumberOfPointsInZ,
                                space=search_grid.Space,
                            ),
                            bottom_tangent_line_z=tangent_lines.BottomTangentLineZ,
                            number_of_tangent_lines=tangent_lines.NumberOfTangentLines,
                            space_tangent_lines=tangent_lines.Space,
                            slip_plane_constraints=DStabilitySlipPlaneConstraints(
                                is_size_constraints_enabled=slip_plane_constraints.IsSizeConstraintsEnabled,
                                is_zone_a_constraints_enabled=slip_plane_constraints.IsZoneAConstraintsEnabled,
                                is_zone_b_constraints_enabled=slip_plane_constraints.IsZoneBConstraintsEnabled,
                                minimum_slip_plane_depth=slip_plane_constraints.MinimumSlipPlaneDepth,
                                minimum_slip_plane_length=slip_plane_constraints.MinimumSlipPlaneLength,
                                width_zone_a=slip_plane_constraints.WidthZoneA,
                                width_zone_b=slip_plane_constraints.WidthZoneB,
                                x_left_zone_a=slip_plane_constraints.XLeftZoneA,
                                x_left_zone_b=slip_plane_constraints.XLeftZoneB,
                            ),
                        )
                    )

        dm.serialize(Path(filename))

    def calculate(self, calculation_name: str):
        from ..external.dstabilitycalculator import DStabilityCalculator

        dsc = DStabilityCalculator(remove_files_afterwards=False)
        dsc.add_model(levee=self, name=calculation_name)
        dsc.calculate()
        return dsc
