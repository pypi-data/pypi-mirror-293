from pollination_dsl.dag import Inputs, DAG, task, Outputs
from dataclasses import dataclass
from pollination.honeybee_radiance_postprocess.abnt import AbntNbr15575Daylight

# input/output alias
from pollination.alias.inputs.model import hbjson_model_input
from pollination.alias.inputs.wea import wea_input
from pollination.alias.inputs.north import north_input
from pollination.alias.inputs.grid import grid_filter_input, \
    min_sensor_count_input, cpu_count
from pollination.alias.inputs.radiancepar import rad_par_daylight_factor_input

from .point_in_time._illuminance import PointInTimeGridEntryPoint
from ._prepare_folder import AbntNbr15575DaylightPrepareFolder
from ._visualization import AbntNbr15575DaylightVisualization


@dataclass
class AbntNbr15575DaylightEntryPoint(DAG):
    """LEED Daylight Illuminance entry point."""

    # inputs
    model = Inputs.file(
        description='A Honeybee model in HBJSON file format.',
        extensions=['json', 'hbjson'],
        alias=hbjson_model_input
    )

    wea = Inputs.file(
        description='A Typical Meteorological Year (TMY) .wea file. The file '
        'must be annual with a timestep of 1 for a non-leap year.',
        extensions=['wea', 'epw'], alias=wea_input
    )

    north = Inputs.float(
        default=0,
        description='A number for rotation from north.',
        spec={'type': 'number', 'minimum': 0, 'maximum': 360},
        alias=north_input
    )

    grid_filter = Inputs.str(
        description='Text for a grid identifier or a pattern to filter the sensor grids '
        'of the model that are simulated. For instance, first_floor_* will simulate '
        'only the sensor grids that have an identifier that starts with '
        'first_floor_. By default, all grids in the model will be simulated.',
        default='*',
        alias=grid_filter_input
    )

    cpu_count = Inputs.int(
        default=50,
        description='The maximum number of CPUs for parallel execution. This will be '
        'used to determine the number of sensors run by each worker.',
        spec={'type': 'integer', 'minimum': 1},
        alias=cpu_count
    )

    min_sensor_count = Inputs.int(
        description='The minimum number of sensors in each sensor grid after '
        'redistributing the sensors based on cpu_count. This value takes '
        'precedence over the cpu_count and can be used to ensure that '
        'the parallelization does not result in generating unnecessarily small '
        'sensor grids. The default value is set to 500.', default=500,
        spec={'type': 'integer', 'minimum': 1},
        alias=min_sensor_count_input
    )

    radiance_parameters = Inputs.str(
        description='The radiance parameters for ray tracing',
        default='-ab 5 -aa 0.1 -ad 2048 -ar 64',
        alias=rad_par_daylight_factor_input
    )

    ground_level = Inputs.float(
        description='A value to define the height of the ground level. This '
        'will make sure that rooms below this height will not be counted as '
        'ground level rooms',
        default=0
    )

    @task(template=AbntNbr15575DaylightPrepareFolder)
    def prepare_folder(
        self, model=model, wea=wea, grid_filter=grid_filter, north=north
        ):
        return [
            {
                'from': AbntNbr15575DaylightPrepareFolder()._outputs.sky_list
            },
            {
                'from': AbntNbr15575DaylightPrepareFolder()._outputs.model_folder,
                'to': 'model'
            },
            {
                'from': AbntNbr15575DaylightPrepareFolder()._outputs.resources,
                'to': 'resources'
            },
            {
                'from': AbntNbr15575DaylightPrepareFolder()._outputs.simulation,
                'to': 'simulation'
            }
        ]

    @task(
        template=PointInTimeGridEntryPoint,
        needs=[prepare_folder],
        loop=prepare_folder._outputs.sky_list,
        sub_folder='simulation/{{item.id}}',
        sub_paths={
            'sky': 'skies/{{item.path}}',
            'sensor_grids_file': 'grids_info.json',
            'bsdfs': 'bsdf'
        }
    )
    def illuminance_simulation(
        self,
        model_folder=prepare_folder._outputs.model_folder,
        sky=prepare_folder._outputs.resources,
        sensor_grids_file=prepare_folder._outputs.resources,
        grid_filter=grid_filter,
        cpu_count=cpu_count,
        min_sensor_count=min_sensor_count,
        radiance_parameters=radiance_parameters,
        bsdfs=prepare_folder._outputs.model_folder
    ):
        # this task doesn't return a folder for each loop.
        # instead we access the results folder as a separate task
        pass

    @task(
        template=AbntNbr15575Daylight,
        needs=[prepare_folder, illuminance_simulation]
    )
    def abnt_nbr_15575_postprocess(
        self, folder=prepare_folder._outputs.simulation, model=model,
        ground_level=ground_level
    ):
        return [
            {
                'from': AbntNbr15575Daylight()._outputs.abnt_nbr_15575,
                'to': 'abnt_nbr_15575'
            }
        ]

    @task(
        template=AbntNbr15575DaylightVisualization,
        needs=[prepare_folder, illuminance_simulation, abnt_nbr_15575_postprocess],
        sub_paths={
            'illuminance_levels': 'illuminance_levels',
            'center_points': 'center_points.json'
        }
    )
    def create_visualization(
        self, model=model, illuminance_4_930am='simulation/4_930AM/results',
        illuminance_4_330pm='simulation/4_330PM/results',
        illuminance_10_930am='simulation/10_930AM/results',
        illuminance_10_330pm='simulation/10_330PM/results',
        illuminance_levels=abnt_nbr_15575_postprocess._outputs.abnt_nbr_15575,
        center_points=abnt_nbr_15575_postprocess._outputs.abnt_nbr_15575
    ):
        return [
            {
                'from': AbntNbr15575DaylightVisualization()._outputs.visualization_illuminance,
                'to': 'visualization_illuminance.vsf'
            },
            {
                'from': AbntNbr15575DaylightVisualization()._outputs.visualization_illuminance_levels,
                'to': 'visualization_illuminance_levels.vsf'
            }
        ]


    abnt_nbr_15575 = Outputs.folder(
        source='abnt_nbr_15575',
        description='Folder with the ABNT NBR 15575 post-processing.'
    )

    abnt_nbr_15575_summary = Outputs.file(
        description='CSV file containing the illuminance level and the '
        'illuminance at the center of the sensor grid.',
        source='abnt_nbr_15575/abnt_nbr_15575_rooms.csv'
    )

    visualization_illuminance = Outputs.file(
        source='visualization_illuminance.vsf',
        description='Visualization in VisualizationSet format.'
    )

    visualization_illuminance_levels = Outputs.file(
        source='visualization_illuminance_levels.vsf',
        description='Visualization in VisualizationSet format.'
    )

    illuminance_april_0930am = Outputs.folder(
        source='simulation/4_930AM/results',
        description='Illuminance results for the 9:30AM (April 23rd) simulation '
        'in lux.'
    )

    illuminance_april_0330pm = Outputs.folder(
        source='simulation/4_330PM/results',
        description='Illuminance results for the 3:30PM (April 23rd) simulation '
        'in lux.'
    )

    illuminance_october_0930am = Outputs.folder(
        source='simulation/10_930AM/results',
        description='Illuminance results for the 9:30AM (October 23rd) simulation '
        'in lux.'
    )

    illuminance_october_0330pm = Outputs.folder(
        source='simulation/10_330PM/results',
        description='Illuminance results for the 3:30PM (October 23rd) simulation '
        'in lux.'
    )
