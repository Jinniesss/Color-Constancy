import numpy as np

from mitsuba import ScalarTransform4f as T

import mitsuba as mi

def initialize_scene():

    d = {
        "type": "scene",
        "integrator": {
            'type': 'path',
            'max_depth': 6,
        },
        
        'sensor': {
            'type': 'perspective',
            'fov_axis': 'smaller',
            'near_clip': 0.001,
            'far_clip': 100.0,
            'focus_distance': 1000,
            'fov': 39.3077,
            'to_world': T.look_at(
                origin=[0, 0, 4],
                target=[0, 0, 0],
                up=[0, 1, 0]
            ),
            'sampler': {
                'type': 'independent',
                'sample_count': 16
            },
            'film': {
                'type': 'hdrfilm',
                'width' : 128,
                'height': 128,
                'rfilter': {
                    'type': 'tent',
                },
                'pixel_format': 'rgb',
                'component_format': 'float32',
            }
        },

        # -------------------- BSDFs --------------------
        'gray': {
            'type': 'diffuse',
            'reflectance': {
                'type': 'rgb',
                'value': [0.85, 0.85, 0.85],
            }
        },
        'color-sphere': {
            'type': 'twosided',
            'material': {
                'type': 'diffuse',
                    'reflectance': {
                    'type': 'rgb',
                    'value': [0.725, 0.71, 0.68],
                }
            }
        },
        'glossy-sphere': {
            'type': 'roughplastic',
            'int_ior': 1.5,                      # Index of refraction (e.g., for plastic)
            'distribution': 'beckmann',
            'alpha': 0.05,                       # LOW ALPHA = HIGH GLOSS (sharp highlights)
            'diffuse_reflectance': {
                # 'type': 'spectrum',
                # 'value': '400:0.8, 550:0.1, 700:0.1' # Example spectral base color (e.g., a reddish spectrum)
                'type': 'rgb',
                'value': [0.725, 0.71, 0.68],
            }
        },
 
        'white': {
            'type': 'diffuse',
            'reflectance': {
                'type': 'rgb',
                'value': [0.885809, 0.698859, 0.666422],
            }
        },
        'green': {
            'type': 'diffuse',
            'reflectance': {
                'type': 'rgb',
                'value': [0.105421, 0.37798, 0.076425],
            }
        },
        'red': {
            'type': 'diffuse',
            'reflectance': {
                'type': 'rgb',
                'value': [0.570068, 0.0430135, 0.0443706],
            }
        },
        # --- small colored patches for the back wall ---
        'patch_red': {
            'type': 'diffuse',
            'reflectance': {
                'type': 'rgb',
                'value': [0.95, 0.05, 0.05],
            }
        },
        'patch_green': {
            'type': 'diffuse',
            'reflectance': {
                'type': 'rgb',
                'value': [0.05, 0.85, 0.05],
            }
        },
        'patch_blue': {
            'type': 'diffuse',
            'reflectance': {
                'type': 'rgb',
                'value': [0.05, 0.05, 0.9],
            }
        },
        'patch_yellow': {
            'type': 'diffuse',
            'reflectance': {
                'type': 'rgb',
                'value': [0.95, 0.9, 0.05],
            }
        },
        'patch_cyan': {
            'type': 'diffuse',
            'reflectance': {
                'type': 'rgb',
                'value': [0.05, 0.85, 0.9],
            }
        },
        'patch_magenta': {
            'type': 'diffuse',
            'reflectance': {
                'type': 'rgb',
                'value': [0.9, 0.05, 0.8],
            }
        },
        
        # -------------------- Light --------------------
        'light': {
            'type': 'rectangle',
            'to_world': T.translate([0.0, 1.6, 1.2]).rotate([1, 0, 0], 90).scale([0.23, 0.19, 0.19]),
            'bsdf': {
                'type': 'ref',
                'id': 'white'
            },
            'emitter': {
                'type': 'area',
                'radiance': {
                    'type': 'rgb',
                    'value': [5*x for x in [18.387, 13.9873, 6.75357]],
                    # 'value': [50, 0, 50],
                }
            }
        },

        'floor': {
            'type': 'obj',
            'filename': 'meshes/cbox_floor.obj',
            'floor-bsdf': {
                'type' : 'ref',
                'id' : 'white'
            }
        },

        # 'ceiling': {
        #     'type': 'obj',
        #     'filename': 'meshes/cbox_ceiling.obj',
        #     'ceiling-bsdf': {
        #         'type' : 'ref',
        #         'id' : 'white'
        #     }
        # },
        
        'back': {
            'type': 'obj',
            'filename': 'meshes/cbox_back.obj',
            'back-bsdf': {
                'type' : 'ref',
                'id' : 'white'
            }
        },

        'greenwall': {
            'type': 'obj',
            'filename': 'meshes/cbox_greenwall.obj',
            'greenwall-bsdf': {
                'type' : 'ref',
                'id' : 'green'
            }
        },
        'redwall': {
            'type': 'obj',
            'filename': 'meshes/cbox_redwall.obj',
            'redwall-bsdf': {
                'type' : 'ref',
                'id' : 'red'
            }
        },
        
        'left-object': {
            'type': 'sphere',
            'to_world': T.translate([0.0, 0.0, -0.3]).scale(0.5),  # [right, up, forward]
            'leftobject-bsdf': {
                'type' : 'ref',
                'id' : 'glossy-sphere'
            }
        },

        # 'right-object': {
        #     'type': 'sphere',
        #     'to_world': T.translate([0.5, -0.75, -0.2]).scale(0.5),
        #     'rightobject-bsdf': {
        #         'type' : 'ref',
        #         'id' : 'color-sphere'
        #     },
        
        # arrange patches in a single horizontal row, smaller and slightly in front of the back wall
        'patch1': {
            'type': 'rectangle',
            'to_world': T.translate([-0.65, 0.8, -0.95]).rotate([0,1,0], 180).scale([0.08, 0.08, 0.08]),
            'bsdf': {
                'type': 'twosided',
                'material': {
                    'type': 'diffuse',
                    'reflectance': {'type': 'rgb', 'value': [0.95, 0.05, 0.05]}
                }
            }
        },
        'patch2': {
            'type': 'rectangle',
            'to_world': T.translate([-0.39, 0.8, -0.95]).rotate([0,1,0], 180).scale([0.08, 0.08, 0.08]),
            'bsdf': {
                'type': 'twosided',
                'material': {
                    'type': 'diffuse',
                    'reflectance': {'type': 'rgb', 'value': [0.05, 0.85, 0.05]}
                }
            }
        },
        'patch3': {
            'type': 'rectangle',
            'to_world': T.translate([-0.13, 0.8, -0.95]).rotate([0,1,0], 180).scale([0.08, 0.08, 0.08]),
            'bsdf': {
                'type': 'twosided',
                'material': {
                    'type': 'diffuse',
                    'reflectance': {'type': 'rgb', 'value': [0.05, 0.05, 0.9]}
                }
            }
        },
        'patch4': {
            'type': 'rectangle',
            'to_world': T.translate([0.13, 0.8, -0.95]).rotate([0,1,0], 180).scale([0.08, 0.08, 0.08]),
            'bsdf': {
                'type': 'twosided',
                'material': {
                    'type': 'diffuse',
                    'reflectance': {'type': 'rgb', 'value': [0.95, 0.9, 0.05]}
                }
            }
        },
        'patch5': {
            'type': 'rectangle',
            'to_world': T.translate([0.39, 0.8, -0.95]).rotate([0,1,0], 180).scale([0.08, 0.08, 0.08]),
            'bsdf': {
                'type': 'twosided',
                'material': {
                    'type': 'diffuse',
                    'reflectance': {'type': 'rgb', 'value': [0.05, 0.85, 0.9]}
                }
            }
        },
        'patch6': {
            'type': 'rectangle',
            'to_world': T.translate([0.65, 0.8, -0.95]).rotate([0,1,0], 180).scale([0.08, 0.08, 0.08]),
            'bsdf': {
                'type': 'twosided',
                'material': {
                    'type': 'diffuse',
                    'reflectance': {'type': 'rgb', 'value': [0.9, 0.05, 0.8]}
                }
            }
        }

    }
    return d

