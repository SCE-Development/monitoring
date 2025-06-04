# TODO: Question life decisions (I'm not sure if this is good)

CPU_BASIC_COLORS = {
    "fieldConfig": {
        "overrides": [
            {
                "matcher": {
                    "id": "byName",
                    "options": "Busy Iowait"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#890F02",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Idle"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#052B51",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Busy Iowait"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#890F02",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Idle"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#7EB26D",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Busy System"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#EAB839",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Busy User"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#0A437C",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Busy Other"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#6D1F62",
                            "mode": "fixed"
                        }
                    }
                ]
            }
        ]
    },
}

MEMORY_BASIC_COLORS = {
    "fieldConfig": {
        "overrides": [
            {
                "matcher": {
                    "id": "byName",
                    "options": "Apps"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#629E51",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Buffers"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#614D93",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Cache"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#6D1F62",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Cached"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#511749",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Committed"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#508642",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Free"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#0A437C",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Hardware Corrupted - Amount of RAM that the kernel identified as corrupted / not working"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#CFFAFF",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Inactive"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#584477",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "PageTables"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#0A50A1",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Page_Tables"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#0A50A1",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "RAM_Free"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#E0F9D7",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "SWAP Used"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#BF1B00",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Slab"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#806EB7",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Slab_Cache"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#E0752D",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Swap"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#BF1B00",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Swap Used"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#BF1B00",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Swap_Cache"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#C15C17",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Swap_Free"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#2F575E",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Unused"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#EAB839",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "RAM Total"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#E0F9D7",
                            "mode": "fixed"
                        }
                    },
                    {
                        "id": "custom.fillOpacity",
                        "value": 0
                    },
                    {
                        "id": "custom.stacking",
                        "value": {
                            "group": False,
                            "mode": "normal"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "RAM Cache + Buffer"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#052B51",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "RAM Free"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#7EB26D",
                            "mode": "fixed"
                        }
                    }
                ]
            },
            {
                "matcher": {
                    "id": "byName",
                    "options": "Available"
                },
                "properties": [
                    {
                        "id": "color",
                        "value": {
                            "fixedColor": "#DEDAF7",
                            "mode": "fixed"
                        }
                    },
                    {
                        "id": "custom.fillOpacity",
                        "value": 0
                    },
                    {
                        "id": "custom.stacking",
                        "value": {
                            "group": False,
                            "mode": "normal"
                        }
                    }
                ]
            }
        ]
    }
}

# Gauge panel configurations for the Quick CPU/Mem/Disk row
GAUGE_CONFIGS = [
    {
        'title': 'CPU Busy',
        'description': 'Overall CPU busy percentage (averaged across all cores)',
        'x_pos': 3,
        'thresholds': [85, 95],
        'expr': '100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle", instance="$instance", job="$job"}[$__rate_interval])))'
    },
    {
        'title': 'Sys Load',
        'description': 'System load over all CPU cores together',
        'x_pos': 6,
        'thresholds': [85, 95],
        'expr': 'scalar(node_load1{instance="$instance",job="$job"}) * 100 / count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu))'
    },
    {
        'title': 'RAM Used',
        'description': 'Real RAM usage excluding cache and reclaimable memory',
        'x_pos': 9,
        'thresholds': [80, 90],
        'expr': '(1 - (node_memory_MemAvailable_bytes{instance="$instance", job="$job"} / node_memory_MemTotal_bytes{instance="$instance", job="$job"})) * 100'
    },
    {
        'title': 'SWAP Used',
        'description': 'Percentage of swap space currently used by the system',
        'x_pos': 12,
        'thresholds': [10, 25],
        'expr': '((node_memory_SwapTotal_bytes{instance="$instance",job="$job"} - node_memory_SwapFree_bytes{instance="$instance",job="$job"}) / (node_memory_SwapTotal_bytes{instance="$instance",job="$job"})) * 100'
    },
    {
        'title': 'Root FS Used',
        'description': 'Used Root FS',
        'x_pos': 15,
        'thresholds': [80, 90],
        'expr': '''(
  (node_filesystem_size_bytes{instance="$instance", job="$job", mountpoint="/", fstype!="rootfs"}
   - node_filesystem_avail_bytes{instance="$instance", job="$job", mountpoint="/", fstype!="rootfs"})
  / node_filesystem_size_bytes{instance="$instance", job="$job", mountpoint="/", fstype!="rootfs"}
) * 100'''
    }
]
