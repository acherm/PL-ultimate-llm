{
  "patcher": {
    "fileversion": 1,
    "appversion": {
      "major": 8,
      "minor": 0,
      "revision": 0
    },
    "rect": [
      100.0,
      100.0,
      400.0,
      300.0
    ],
    "boxes": [
      {
        "box": {
          "maxclass": "message",
          "text": "Hello World",
          "patching_rect": [
            50.0,
            50.0,
            100.0,
            22.0
          ],
          "id": "obj-1"
        }
      },
      {
        "box": {
          "maxclass": "button",
          "patching_rect": [
            50.0,
            20.0,
            24.0,
            24.0
          ],
          "id": "obj-2"
        }
      },
      {
        "box": {
          "maxclass": "print",
          "patching_rect": [
            50.0,
            100.0,
            50.0,
            22.0
          ],
          "id": "obj-3"
        }
      }
    ],
    "lines": [
      {
        "patchline": {
          "source": [
            "obj-2",
            0
          ],
          "destination": [
            "obj-1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-1",
            0
          ],
          "destination": [
            "obj-3",
            0
          ]
        }
      }
    ]
  }
}