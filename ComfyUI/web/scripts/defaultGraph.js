export const defaultGraph ={
  "last_node_id": 177,
  "last_link_id": 248,
  "nodes": [
    {
      "id": 10,
      "type": "CLIPSetLastLayer",
      "pos": [
        -660,
        -30
      ],
      "size": {
        "0": 315,
        "1": 58
      },
      "flags": {},
      "order": 39,
      "mode": 0,
      "inputs": [
        {
          "name": "clip",
          "type": "CLIP",
          "link": 78
        }
      ],
      "outputs": [
        {
          "name": "CLIP",
          "type": "CLIP",
          "links": [
            11,
            12
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "CLIPSetLastLayer"
      },
      "widgets_values": [
        -2
      ]
    },
    {
      "id": 6,
      "type": "CLIPTextEncode",
      "pos": [
        -250,
        -140
      ],
      "size": {
        "0": 480.5587463378906,
        "1": 188.92535400390625
      },
      "flags": {},
      "order": 56,
      "mode": 0,
      "inputs": [
        {
          "name": "clip",
          "type": "CLIP",
          "link": 11
        }
      ],
      "outputs": [
        {
          "name": "CONDITIONING",
          "type": "CONDITIONING",
          "links": [
            80
          ],
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "CLIPTextEncode"
      },
      "widgets_values": [
        "Boris Karloff, evil smile, portrait from above, sinister grin, messy charcoal scribble, , sinister, teeth showing, wearing a suit, balding, old, white background, close-up"
      ]
    },
    {
      "id": 55,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        -150,
        1020
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 40,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 95,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            82
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 57,
      "type": "TimestepKeyframe",
      "pos": [
        -740,
        1030
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 22,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 87,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            95
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 7,
      "type": "CLIPTextEncode",
      "pos": [
        -250,
        90
      ],
      "size": {
        "0": 483.6921691894531,
        "1": 182.32534790039062
      },
      "flags": {},
      "order": 57,
      "mode": 0,
      "inputs": [
        {
          "name": "clip",
          "type": "CLIP",
          "link": 12
        }
      ],
      "outputs": [
        {
          "name": "CONDITIONING",
          "type": "CONDITIONING",
          "links": [
            81
          ],
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "CLIPTextEncode"
      },
      "widgets_values": [
        "(worst quality, low quality:1.4)"
      ]
    },
    {
      "id": 69,
      "type": "TimestepKeyframe",
      "pos": [
        -720,
        1240
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 23,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 105,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            104
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 74,
      "type": "TimestepKeyframe",
      "pos": [
        -700,
        1450
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 24,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 117,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            116
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 79,
      "type": "TimestepKeyframe",
      "pos": [
        -670,
        1650
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 25,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 121,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            120
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 89,
      "type": "TimestepKeyframe",
      "pos": [
        -690,
        2050
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 27,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 129,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            128
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 94,
      "type": "TimestepKeyframe",
      "pos": [
        -690,
        2250
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 28,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 133,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            132
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 99,
      "type": "TimestepKeyframe",
      "pos": [
        -700,
        2410
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 29,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 137,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            136
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 84,
      "type": "TimestepKeyframe",
      "pos": [
        -680,
        1850
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 26,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 125,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            124
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 68,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        -130,
        1230
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 41,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 104,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            102
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 73,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        -110,
        1440
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 42,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 116,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            114
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 78,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        -80,
        1640
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 43,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 120,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            118
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 83,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        -90,
        1840
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 44,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 124,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            122
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 88,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        -100,
        2040
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 45,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 128,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            126
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 93,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        -100,
        2240
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 46,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 132,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            130
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 98,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        -110,
        2400
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 47,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 136,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            134
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 54,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        610,
        820
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 58,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 80
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 81
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 82,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 96
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            110
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            111
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        1,
        0,
        1
      ]
    },
    {
      "id": 143,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        1470,
        3080
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 54,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 200,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            198
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 144,
      "type": "TimestepKeyframe",
      "pos": [
        880,
        3090
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 36,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 201,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            200
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 148,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        1490,
        3290
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 55,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 206,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            204
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 149,
      "type": "TimestepKeyframe",
      "pos": [
        900,
        3300
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 37,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 207,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            206
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 152,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        1510,
        3500
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 48,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 212,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            210
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 153,
      "type": "TimestepKeyframe",
      "pos": [
        920,
        3510
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 30,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 213,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            212
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 156,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        1540,
        3700
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 49,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 218,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            216
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 157,
      "type": "TimestepKeyframe",
      "pos": [
        950,
        3710
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 31,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 219,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            218
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 160,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        1530,
        3900
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 50,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 224,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            222
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 161,
      "type": "TimestepKeyframe",
      "pos": [
        940,
        3910
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 32,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 225,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            224
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 164,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        1520,
        4100
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 51,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 230,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            228
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 165,
      "type": "TimestepKeyframe",
      "pos": [
        930,
        4110
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 33,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 231,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            230
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 168,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        1520,
        4300
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 52,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 236,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            234
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 169,
      "type": "TimestepKeyframe",
      "pos": [
        930,
        4310
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 34,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 237,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            236
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 172,
      "type": "ControlNetLoaderAdvanced",
      "pos": [
        1510,
        4460
      ],
      "size": {
        "0": 367.79998779296875,
        "1": 58
      },
      "flags": {},
      "order": 53,
      "mode": 0,
      "inputs": [
        {
          "name": "timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": 242,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "CONTROL_NET",
          "type": "CONTROL_NET",
          "links": [
            240
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetLoaderAdvanced"
      },
      "widgets_values": [
        "control_v11f1e_sd15_tile.pth"
      ]
    },
    {
      "id": 173,
      "type": "TimestepKeyframe",
      "pos": [
        920,
        4470
      ],
      "size": {
        "0": 506.4000244140625,
        "1": 118
      },
      "flags": {},
      "order": 35,
      "mode": 0,
      "inputs": [
        {
          "name": "control_net_weights",
          "type": "CONTROL_NET_WEIGHTS",
          "link": null
        },
        {
          "name": "t2i_adapter_weights",
          "type": "T2I_ADAPTER_WEIGHTS",
          "link": null
        },
        {
          "name": "latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": 243,
          "slot_index": 2
        },
        {
          "name": "prev_timestep_keyframe",
          "type": "TIMESTEP_KEYFRAME",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "TIMESTEP_KEYFRAME",
          "type": "TIMESTEP_KEYFRAME",
          "links": [
            242
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "TimestepKeyframe"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 49,
      "type": "KSampler",
      "pos": [
        2780,
        4760
      ],
      "size": {
        "0": 315,
        "1": 474
      },
      "flags": {},
      "order": 74,
      "mode": 0,
      "inputs": [
        {
          "name": "model",
          "type": "MODEL",
          "link": 90,
          "slot_index": 0
        },
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 246
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 247,
          "slot_index": 2
        },
        {
          "name": "latent_image",
          "type": "LATENT",
          "link": 92
        }
      ],
      "outputs": [
        {
          "name": "LATENT",
          "type": "LATENT",
          "links": [
            75
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "KSampler"
      },
      "widgets_values": [
        611488905974512,
        "randomize",
        20,
        7,
        "dpmpp_2m",
        "karras",
        1
      ]
    },
    {
      "id": 58,
      "type": "LatentKeyframe",
      "pos": [
        -1280,
        1070
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 0,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            87
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        0,
        1
      ]
    },
    {
      "id": 5,
      "type": "EmptyLatentImage",
      "pos": [
        2754,
        4195
      ],
      "size": {
        "0": 315,
        "1": 106
      },
      "flags": {},
      "order": 1,
      "mode": 0,
      "outputs": [
        {
          "name": "LATENT",
          "type": "LATENT",
          "links": [
            91
          ],
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "EmptyLatentImage"
      },
      "widgets_values": [
        512,
        512,
        16
      ]
    },
    {
      "id": 70,
      "type": "LatentKeyframe",
      "pos": [
        -1260,
        1280
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 2,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            105
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        1,
        1
      ]
    },
    {
      "id": 75,
      "type": "LatentKeyframe",
      "pos": [
        -1240,
        1490
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 3,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            117
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        2,
        1
      ]
    },
    {
      "id": 80,
      "type": "LatentKeyframe",
      "pos": [
        -1210,
        1690
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 4,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            121
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        3,
        1
      ]
    },
    {
      "id": 85,
      "type": "LatentKeyframe",
      "pos": [
        -1220,
        1890
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 5,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            125
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        4,
        1
      ]
    },
    {
      "id": 90,
      "type": "LatentKeyframe",
      "pos": [
        -1230,
        2090
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 6,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            129
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        5,
        1
      ]
    },
    {
      "id": 95,
      "type": "LatentKeyframe",
      "pos": [
        -1230,
        2290
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 7,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            133
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        6,
        1
      ]
    },
    {
      "id": 100,
      "type": "LatentKeyframe",
      "pos": [
        -1239,
        2450
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 8,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            137
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        7,
        1
      ]
    },
    {
      "id": 154,
      "type": "LatentKeyframe",
      "pos": [
        380,
        3550
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 9,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            213
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        10,
        1
      ]
    },
    {
      "id": 158,
      "type": "LatentKeyframe",
      "pos": [
        410,
        3750
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 10,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            219
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        11,
        1
      ]
    },
    {
      "id": 162,
      "type": "LatentKeyframe",
      "pos": [
        400,
        3950
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 11,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            225
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        12,
        1
      ]
    },
    {
      "id": 166,
      "type": "LatentKeyframe",
      "pos": [
        390,
        4150
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 12,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            231
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        13,
        1
      ]
    },
    {
      "id": 170,
      "type": "LatentKeyframe",
      "pos": [
        390,
        4350
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 13,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            237
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        14,
        1
      ]
    },
    {
      "id": 174,
      "type": "LatentKeyframe",
      "pos": [
        380,
        4510
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 14,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            243
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        15,
        1
      ]
    },
    {
      "id": 67,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        600,
        1080
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 59,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 110
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 111
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 102,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 189
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            175
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            176
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        0.6,
        0,
        1
      ]
    },
    {
      "id": 72,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        600,
        1330
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 60,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 175
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 176
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 114,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 190
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            177
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            178
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        0.5,
        0,
        1
      ]
    },
    {
      "id": 77,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        580,
        1560
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 61,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 177
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 178
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 118,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 191
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            179
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            180
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        0.4,
        0,
        1
      ]
    },
    {
      "id": 82,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        570,
        1800
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 62,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 179
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 180
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 122,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 192
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            181
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            182
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        0.3,
        0,
        1
      ]
    },
    {
      "id": 87,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        560,
        2039
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 63,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 181
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 182
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 126,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 193
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            183
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            184
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        0.2,
        0,
        1
      ]
    },
    {
      "id": 92,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        550,
        2270
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 64,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 183
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 184
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 130,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 194
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            185
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            186
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        0.1,
        0,
        1
      ]
    },
    {
      "id": 97,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        550,
        2500
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 65,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 185
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 186
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 134,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 195
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            244
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            245
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        0.05,
        0,
        1
      ]
    },
    {
      "id": 145,
      "type": "LatentKeyframe",
      "pos": [
        340,
        3130
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 15,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            201
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        8,
        1
      ]
    },
    {
      "id": 150,
      "type": "LatentKeyframe",
      "pos": [
        360,
        3340
      ],
      "size": {
        "0": 456,
        "1": 82
      },
      "flags": {},
      "order": 16,
      "mode": 0,
      "inputs": [
        {
          "name": "prev_latent_keyframe",
          "type": "LATENT_KEYFRAME",
          "link": null,
          "slot_index": 0
        }
      ],
      "outputs": [
        {
          "name": "LATENT_KEYFRAME",
          "type": "LATENT_KEYFRAME",
          "links": [
            207
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LatentKeyframe"
      },
      "widgets_values": [
        9,
        1
      ]
    },
    {
      "id": 142,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        2230,
        2880
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 66,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 244
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 245
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 198,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 199
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            202
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            203
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        0.1,
        0,
        1
      ]
    },
    {
      "id": 147,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        2220,
        3140
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 67,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 202
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 203
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 204,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 205
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            208
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            209
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        0.2,
        0,
        1
      ]
    },
    {
      "id": 151,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        2220,
        3390
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 68,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 208
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 209
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 210,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 211
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            214
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            215
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        0.3,
        0,
        1
      ]
    },
    {
      "id": 155,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        2200,
        3620
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 69,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 214
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 215
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 216,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 217
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            220
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            221
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        0.4,
        0,
        1
      ]
    },
    {
      "id": 159,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        2190,
        3860
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 70,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 220
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 221
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 222,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 223
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            226
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            227
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        0.5,
        0,
        1
      ]
    },
    {
      "id": 163,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        2180,
        4100
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 71,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 226
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 227
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 228,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 229
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            232
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            233
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        0.6,
        0,
        1
      ]
    },
    {
      "id": 167,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        2170,
        4330
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 72,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 232
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 233
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 234,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 235
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            238
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            239
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        0.7,
        0,
        1
      ]
    },
    {
      "id": 171,
      "type": "ControlNetApplyAdvanced",
      "pos": [
        2168,
        4556
      ],
      "size": {
        "0": 315,
        "1": 166
      },
      "flags": {},
      "order": 73,
      "mode": 0,
      "inputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 238
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 239
        },
        {
          "name": "control_net",
          "type": "CONTROL_NET",
          "link": 240,
          "slot_index": 2
        },
        {
          "name": "image",
          "type": "IMAGE",
          "link": 241
        }
      ],
      "outputs": [
        {
          "name": "positive",
          "type": "CONDITIONING",
          "links": [
            246
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "links": [
            247
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "ControlNetApplyAdvanced"
      },
      "widgets_values": [
        1,
        0,
        1
      ]
    },
    {
      "id": 64,
      "type": "LoadImage",
      "pos": [
        -251,
        603
      ],
      "size": {
        "0": 315,
        "1": 314
      },
      "flags": {},
      "order": 17,
      "mode": 0,
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            96,
            189,
            190,
            191,
            192,
            193,
            194,
            195
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "MASK",
          "type": "MASK",
          "links": null,
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LoadImage"
      },
      "widgets_values": [
        "1.jpg",
        "image"
      ]
    },
    {
      "id": 176,
      "type": "Note",
      "pos": [
        -338,
        -595
      ],
      "size": {
        "0": 315.5848083496094,
        "1": 258.3334655761719
      },
      "flags": {},
      "order": 18,
      "mode": 0,
      "properties": {
        "text": ""
      },
      "widgets_values": [
        "This is an example workflow for interpolating between two images. \n\nYou can find more example workflows here: https://github.com/Kosinkadink/ComfyUI-AnimateDiff"
      ],
      "color": "#432",
      "bgcolor": "#653"
    },
    {
      "id": 11,
      "type": "VAELoader",
      "pos": [
        -900,
        290
      ],
      "size": {
        "0": 210,
        "1": 58
      },
      "flags": {},
      "order": 19,
      "mode": 0,
      "outputs": [
        {
          "name": "VAE",
          "type": "VAE",
          "links": [
            13
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "VAELoader"
      },
      "widgets_values": [
        "vae-ft-mse-840000-ema-pruned.safetensors"
      ]
    },
    {
      "id": 52,
      "type": "CheckpointLoaderSimpleWithNoiseSelect",
      "pos": [
        -1030,
        60
      ],
      "size": {
        "0": 315,
        "1": 122
      },
      "flags": {},
      "order": 20,
      "mode": 0,
      "outputs": [
        {
          "name": "MODEL",
          "type": "MODEL",
          "links": [
            89
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "CLIP",
          "type": "CLIP",
          "links": [
            78
          ],
          "shape": 3,
          "slot_index": 1
        },
        {
          "name": "VAE",
          "type": "VAE",
          "links": null,
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "CheckpointLoaderSimpleWithNoiseSelect"
      },
      "widgets_values": [
        "Realistic_Vision_V5.0.safetensors",
        "sqrt_linear (AnimateDiff)"
      ]
    },
    {
      "id": 8,
      "type": "VAEDecode",
      "pos": [
        3120,
        4750
      ],
      "size": {
        "0": 210,
        "1": 46
      },
      "flags": {},
      "order": 75,
      "mode": 0,
      "inputs": [
        {
          "name": "samples",
          "type": "LATENT",
          "link": 75
        },
        {
          "name": "vae",
          "type": "VAE",
          "link": 13
        }
      ],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            65,
            248
          ],
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "VAEDecode"
      }
    },
    {
      "id": 60,
      "type": "AnimateDiffLoaderV1",
      "pos": [
        2760,
        4379
      ],
      "size": {
        "0": 315,
        "1": 150
      },
      "flags": {},
      "order": 38,
      "mode": 0,
      "inputs": [
        {
          "name": "model",
          "type": "MODEL",
          "link": 89
        },
        {
          "name": "latents",
          "type": "LATENT",
          "link": 91
        }
      ],
      "outputs": [
        {
          "name": "MODEL",
          "type": "MODEL",
          "links": [
            90
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "LATENT",
          "type": "LATENT",
          "links": [
            92
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "AnimateDiffLoaderV1"
      },
      "widgets_values": [
        "mm-Stabilized_mid.ckpt",
        false
      ]
    },
    {
      "id": 146,
      "type": "LoadImage",
      "pos": [
        1128,
        2663
      ],
      "size": {
        "0": 315,
        "1": 314
      },
      "flags": {},
      "order": 21,
      "mode": 0,
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            199,
            205,
            211,
            217,
            223,
            229,
            235,
            241
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "MASK",
          "type": "MASK",
          "links": null,
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LoadImage"
      },
      "widgets_values": [
        "2.jpg",
        "image"
      ]
    },
    {
      "id": 35,
      "type": "PreviewImage",
      "pos": [
        3401,
        4892
      ],
      "size": {
        "0": 612.9501342773438,
        "1": 608.2142333984375
      },
      "flags": {},
      "order": 76,
      "mode": 0,
      "inputs": [
        {
          "name": "images",
          "type": "IMAGE",
          "link": 65,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "PreviewImage"
      }
    },
    {
      "id": 177,
      "type": "ADE_AnimateDiffCombine",
      "pos": [
        3693,
        4540
      ],
      "size": {
        "0": 315,
        "1": 130
      },
      "flags": {},
      "order": 77,
      "mode": 0,
      "inputs": [
        {
          "name": "images",
          "type": "IMAGE",
          "link": 248
        }
      ],
      "properties": {
        "Node name for S&R": "ADE_AnimateDiffCombine"
      },
      "widgets_values": [
        16,
        0,
        "Enabled",
        "AnimateDiff"
      ]
    }
  ],
  "links": [
    [
      11,
      10,
      0,
      6,
      0,
      "CLIP"
    ],
    [
      12,
      10,
      0,
      7,
      0,
      "CLIP"
    ],
    [
      13,
      11,
      0,
      8,
      1,
      "VAE"
    ],
    [
      65,
      8,
      0,
      35,
      0,
      "IMAGE"
    ],
    [
      75,
      49,
      0,
      8,
      0,
      "LATENT"
    ],
    [
      78,
      52,
      1,
      10,
      0,
      "CLIP"
    ],
    [
      80,
      6,
      0,
      54,
      0,
      "CONDITIONING"
    ],
    [
      81,
      7,
      0,
      54,
      1,
      "CONDITIONING"
    ],
    [
      82,
      55,
      0,
      54,
      2,
      "CONTROL_NET"
    ],
    [
      87,
      58,
      0,
      57,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      89,
      52,
      0,
      60,
      0,
      "MODEL"
    ],
    [
      90,
      60,
      0,
      49,
      0,
      "MODEL"
    ],
    [
      91,
      5,
      0,
      60,
      1,
      "LATENT"
    ],
    [
      92,
      60,
      1,
      49,
      3,
      "LATENT"
    ],
    [
      95,
      57,
      0,
      55,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      96,
      64,
      0,
      54,
      3,
      "IMAGE"
    ],
    [
      102,
      68,
      0,
      67,
      2,
      "CONTROL_NET"
    ],
    [
      104,
      69,
      0,
      68,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      105,
      70,
      0,
      69,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      110,
      54,
      0,
      67,
      0,
      "CONDITIONING"
    ],
    [
      111,
      54,
      1,
      67,
      1,
      "CONDITIONING"
    ],
    [
      114,
      73,
      0,
      72,
      2,
      "CONTROL_NET"
    ],
    [
      116,
      74,
      0,
      73,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      117,
      75,
      0,
      74,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      118,
      78,
      0,
      77,
      2,
      "CONTROL_NET"
    ],
    [
      120,
      79,
      0,
      78,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      121,
      80,
      0,
      79,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      122,
      83,
      0,
      82,
      2,
      "CONTROL_NET"
    ],
    [
      124,
      84,
      0,
      83,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      125,
      85,
      0,
      84,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      126,
      88,
      0,
      87,
      2,
      "CONTROL_NET"
    ],
    [
      128,
      89,
      0,
      88,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      129,
      90,
      0,
      89,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      130,
      93,
      0,
      92,
      2,
      "CONTROL_NET"
    ],
    [
      132,
      94,
      0,
      93,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      133,
      95,
      0,
      94,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      134,
      98,
      0,
      97,
      2,
      "CONTROL_NET"
    ],
    [
      136,
      99,
      0,
      98,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      137,
      100,
      0,
      99,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      175,
      67,
      0,
      72,
      0,
      "CONDITIONING"
    ],
    [
      176,
      67,
      1,
      72,
      1,
      "CONDITIONING"
    ],
    [
      177,
      72,
      0,
      77,
      0,
      "CONDITIONING"
    ],
    [
      178,
      72,
      1,
      77,
      1,
      "CONDITIONING"
    ],
    [
      179,
      77,
      0,
      82,
      0,
      "CONDITIONING"
    ],
    [
      180,
      77,
      1,
      82,
      1,
      "CONDITIONING"
    ],
    [
      181,
      82,
      0,
      87,
      0,
      "CONDITIONING"
    ],
    [
      182,
      82,
      1,
      87,
      1,
      "CONDITIONING"
    ],
    [
      183,
      87,
      0,
      92,
      0,
      "CONDITIONING"
    ],
    [
      184,
      87,
      1,
      92,
      1,
      "CONDITIONING"
    ],
    [
      185,
      92,
      0,
      97,
      0,
      "CONDITIONING"
    ],
    [
      186,
      92,
      1,
      97,
      1,
      "CONDITIONING"
    ],
    [
      189,
      64,
      0,
      67,
      3,
      "IMAGE"
    ],
    [
      190,
      64,
      0,
      72,
      3,
      "IMAGE"
    ],
    [
      191,
      64,
      0,
      77,
      3,
      "IMAGE"
    ],
    [
      192,
      64,
      0,
      82,
      3,
      "IMAGE"
    ],
    [
      193,
      64,
      0,
      87,
      3,
      "IMAGE"
    ],
    [
      194,
      64,
      0,
      92,
      3,
      "IMAGE"
    ],
    [
      195,
      64,
      0,
      97,
      3,
      "IMAGE"
    ],
    [
      198,
      143,
      0,
      142,
      2,
      "CONTROL_NET"
    ],
    [
      199,
      146,
      0,
      142,
      3,
      "IMAGE"
    ],
    [
      200,
      144,
      0,
      143,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      201,
      145,
      0,
      144,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      202,
      142,
      0,
      147,
      0,
      "CONDITIONING"
    ],
    [
      203,
      142,
      1,
      147,
      1,
      "CONDITIONING"
    ],
    [
      204,
      148,
      0,
      147,
      2,
      "CONTROL_NET"
    ],
    [
      205,
      146,
      0,
      147,
      3,
      "IMAGE"
    ],
    [
      206,
      149,
      0,
      148,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      207,
      150,
      0,
      149,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      208,
      147,
      0,
      151,
      0,
      "CONDITIONING"
    ],
    [
      209,
      147,
      1,
      151,
      1,
      "CONDITIONING"
    ],
    [
      210,
      152,
      0,
      151,
      2,
      "CONTROL_NET"
    ],
    [
      211,
      146,
      0,
      151,
      3,
      "IMAGE"
    ],
    [
      212,
      153,
      0,
      152,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      213,
      154,
      0,
      153,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      214,
      151,
      0,
      155,
      0,
      "CONDITIONING"
    ],
    [
      215,
      151,
      1,
      155,
      1,
      "CONDITIONING"
    ],
    [
      216,
      156,
      0,
      155,
      2,
      "CONTROL_NET"
    ],
    [
      217,
      146,
      0,
      155,
      3,
      "IMAGE"
    ],
    [
      218,
      157,
      0,
      156,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      219,
      158,
      0,
      157,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      220,
      155,
      0,
      159,
      0,
      "CONDITIONING"
    ],
    [
      221,
      155,
      1,
      159,
      1,
      "CONDITIONING"
    ],
    [
      222,
      160,
      0,
      159,
      2,
      "CONTROL_NET"
    ],
    [
      223,
      146,
      0,
      159,
      3,
      "IMAGE"
    ],
    [
      224,
      161,
      0,
      160,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      225,
      162,
      0,
      161,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      226,
      159,
      0,
      163,
      0,
      "CONDITIONING"
    ],
    [
      227,
      159,
      1,
      163,
      1,
      "CONDITIONING"
    ],
    [
      228,
      164,
      0,
      163,
      2,
      "CONTROL_NET"
    ],
    [
      229,
      146,
      0,
      163,
      3,
      "IMAGE"
    ],
    [
      230,
      165,
      0,
      164,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      231,
      166,
      0,
      165,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      232,
      163,
      0,
      167,
      0,
      "CONDITIONING"
    ],
    [
      233,
      163,
      1,
      167,
      1,
      "CONDITIONING"
    ],
    [
      234,
      168,
      0,
      167,
      2,
      "CONTROL_NET"
    ],
    [
      235,
      146,
      0,
      167,
      3,
      "IMAGE"
    ],
    [
      236,
      169,
      0,
      168,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      237,
      170,
      0,
      169,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      238,
      167,
      0,
      171,
      0,
      "CONDITIONING"
    ],
    [
      239,
      167,
      1,
      171,
      1,
      "CONDITIONING"
    ],
    [
      240,
      172,
      0,
      171,
      2,
      "CONTROL_NET"
    ],
    [
      241,
      146,
      0,
      171,
      3,
      "IMAGE"
    ],
    [
      242,
      173,
      0,
      172,
      0,
      "TIMESTEP_KEYFRAME"
    ],
    [
      243,
      174,
      0,
      173,
      2,
      "LATENT_KEYFRAME"
    ],
    [
      244,
      97,
      0,
      142,
      0,
      "CONDITIONING"
    ],
    [
      245,
      97,
      1,
      142,
      1,
      "CONDITIONING"
    ],
    [
      246,
      171,
      0,
      49,
      1,
      "CONDITIONING"
    ],
    [
      247,
      171,
      1,
      49,
      2,
      "CONDITIONING"
    ],
    [
      248,
      8,
      0,
      177,
      0,
      "IMAGE"
    ]
  ],
  "groups": [],
  "config": {},
  "extra": {},
  "version": 0.4
};