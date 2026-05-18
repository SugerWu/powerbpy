"""Dual axis chart (组合图) for Power BI dashboards.
Supports combining a column chart with a line chart on the same page,
each with its own Y-axis.
This class is used to represent dual axis charts that can be added to pages.
You should never call this class directly, instead use the add_dual_axis_chart() method attached to the _Page class.
See add_dual_axis_chart() for more details.
"""

import json
import uuid

from powerbpy.visual import _Visual

class _DualAxisChart(_Visual):
    """A dual axis chart (column + line) visual type for Power BI."""

    def __init__(self,
                 page,
                 *,
                 visual_id,
                 data_source,
                 visual_title,
                 x_axis_title,
                 y_axis_title_left,
                 y_axis_title_right,
                 x_axis_var,
                 col_y_axis_var,
                 col_y_axis_var_aggregation_type,
                 line_y_axis_var,
                 line_y_axis_var_aggregation_type,
                 x_position,
                 y_position,
                 height,
                 width,
                 tab_order,
                 z_position,
                 parent_group_id,
                 background_color,
                 background_color_alpha,
                 show_data_labels=False,
                 show_x_axis=True,
                 show_y_axis_left=True,
                 show_y_axis_right=True,
                 legend_position='Bottom',
                 alt_text='A dual axis chart'):

        super().__init__(page=page,
                         visual_id=visual_id,
                         visual_title=visual_title,
                         height=height,
                         width=width,
                         x_position=x_position,
                         y_position=y_position,
                         z_position=z_position,
                         tab_order=tab_order,
                         parent_group_id=parent_group_id,
                         alt_text=alt_text,
                         background_color=background_color,
                         background_color_alpha=background_color_alpha)

        # Dual axis chart visual type
        self.visual_json['visual']['visualType'] = 'dualAxisChart'

        # Build the query definition with two series
        self.visual_json['visual']['query'] = {
            'queryState': {
                'Category': {
                    'projections': [
                        {
                            'field': {
                                'Column': {
                                    'Expression': {
                                        'SourceRef': {
                                            'Entity': data_source
                                        }
                                    },
                                    'Property': x_axis_var
                                }
                            },
                            'queryRef': f'{data_source}.{x_axis_var}',
                            'nativeQueryRef': x_axis_var,
                            'active': True
                        }
                    ]
                },
                'Y': {
                    'projections': [
                        {
                            'field': {
                                'Aggregation': {
                                    'Expression': {
                                        'Column': {
                                            'Expression': {
                                                'SourceRef': {
                                                    'Entity': data_source
                                                }
                                            },
                                            'Property': col_y_axis_var
                                        }
                                    },
                                    'Function': 0
                                }
                            },
                            'queryRef': f'{col_y_axis_var_aggregation_type}({data_source}.{col_y_axis_var})',
                            'nativeQueryRef': f'{col_y_axis_var_aggregation_type} of {col_y_axis_var}'
                        }
                    ]
                },
                'Y2': {
                    'projections': [
                        {
                            'field': {
                                'Aggregation': {
                                    'Expression': {
                                        'Column': {
                                            'Expression': {
                                                'SourceRef': {
                                                    'Entity': data_source
                                                }
                                            },
                                            'Property': line_y_axis_var
                                        }
                                    },
                                    'Function': 0
                                }
                            },
                            'queryRef': f'{line_y_axis_var_aggregation_type}({data_source}.{line_y_axis_var})',
                            'nativeQueryRef': f'{line_y_axis_var_aggregation_type} of {line_y_axis_var}'
                        }
                    ]
                }
            },
            'sortDefinition': {
                'sort': [
                    {
                        'field': {
                            'Column': {
                                'Expression': {
                                    'SourceRef': {
                                        'Entity': data_source
                                    }
                                },
                                'Property': x_axis_var
                            }
                        },
                        'direction': 'Ascending'
                    }
                ],
                'isDefaultSort': True
            }
        }

        # Build objects (styling)
        self.visual_json['visual']['objects'] = {
            'categoryAxis': [
                {
                    'properties': {
                        'show': {'expr': {'Literal': {'Value': f'{"true" if show_x_axis else "false"}'}}},
                        'titleText': {
                            'expr': {'Literal': {'Value': f"'{x_axis_title}'"}}
                        }
                    }
                }
            ],
            'valueAxis': [
                {
                    'properties': {
                        'show': {'expr': {'Literal': {'Value': f'{"true" if show_y_axis_left else "false"}'}}},
                        'titleText': {
                            'expr': {'Literal': {'Value': f"'{y_axis_title_left}'"}}
                        }
                    }
                }
            ],
            'valueAxis2': [
                {
                    'properties': {
                        'show': {'expr': {'Literal': {'Value': f'{"true" if show_y_axis_right else "false"}'}}},
                        'titleText': {
                            'expr': {'Literal': {'Value': f"'{y_axis_title_right}'"}}
                        }
                    }
                }
            ],
            'legend': [
                {
                    'properties': {
                        'show': {'expr': {'Literal': {'Value': 'true'}}},
                        'position': {'expr': {'Literal': {'Value': f"'{legend_position}'"}}}
                    }
                }
            ],
            'dataLabels': [
                {
                    'properties': {
                        'show': {'expr': {'Literal': {'Value': 'true' if show_data_labels else 'false'}}}
                    }
                }
            ]
        }

        # Write out the JSON
        with open(self.visual_json_path, 'w', encoding='utf-8') as file:
            json.dump(self.visual_json, file, indent=2)
