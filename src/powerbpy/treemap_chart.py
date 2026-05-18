"""Treemap chart visual for Power BI dashboards.
This class is used to represent treemaps that can be added to pages.
You should never call this class directly, instead use the add_treemap_chart() method attached to the _Page class.
See add_treemap_chart() for more details.
"""

import json

from powerbpy.visual import _Visual

class _TreemapChart(_Visual):
    """A treemap chart visual type for Power BI."""

    def __init__(self,
                 page,
                 *,
                 visual_id,
                 data_source,
                 visual_title,
                 category_var,
                 value_var,
                 value_var_aggregation_type,
                 x_position,
                 y_position,
                 height,
                 width,
                 tab_order,
                 z_position,
                 parent_group_id,
                 background_color,
                 background_color_alpha,
                 show_data_labels=True,
                 show_legend=True,
                 color_palette='Auto',
                 sort_by='Descending',
                 sort_field=None,
                 alt_text='A treemap chart'):

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

        # Set visual type
        self.visual_json['visual']['visualType'] = 'treemap'

        # Build the query definition
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
                                    'Property': category_var
                                }
                            },
                            'queryRef': f'{data_source}.{category_var}',
                            'nativeQueryRef': category_var,
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
                                            'Property': value_var
                                        }
                                    },
                                    'Function': 0
                                }
                            },
                            'queryRef': f'{value_var_aggregation_type}({data_source}.{value_var})',
                            'nativeQueryRef': f'{value_var_aggregation_type} of {value_var}'
                        }
                    ]
                }
            },
            'sortDefinition': {
                'sort': [
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
                                        'Property': value_var
                                    }
                                },
                                'Function': 0
                            }
                        },
                        'direction': 'Descending' if sort_by == 'Descending' else 'Ascending'
                    }
                ],
                'isDefaultSort': True
            }
        }

        # Build objects (styling)
        self.visual_json['visual']['objects'] = {
            'legend': [
                {
                    'properties': {
                        'show': {'expr': {'Literal': {'Value': 'true' if show_legend else 'false'}}}
                    }
                }
            ],
            'dataLabels': [
                {
                    'properties': {
                        'show': {'expr': {'Literal': {'Value': 'true' if show_data_labels else 'false'}}}
                    }
                }
            ],
            'categoryLabels': [
                {
                    'properties': {
                        'show': {'expr': {'Literal': {'Value': 'true'}}}
                    }
                }
            ],
            'values': [
                {
                    'properties': {
                        'color': {
                            'solid': {
                                'color': {
                                    'expr': {
                                        'Literal': {
                                            'Value': f"'{color_palette}'"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            ]
        }

        # Write out the JSON
        with open(self.visual_json_path, 'w', encoding='utf-8') as file:
            json.dump(self.visual_json, file, indent=2)
