import QtQuick
import Quickshell.Io
import qs.Ui

// Command module whose text color follows the Waybar-style "class" the script
// prints, e.g. cpu-detailed.py (good/medium/warning/critical) or weather.py
// (frio/ameno/quente/...). Settings in shell.json:
//   exec, interval (s), colors {class: "#rrggbb"}, bold, onClick, onRightClick, onMiddleClick
Item {
  id: root

  property var bar
  property string moduleName
  property var settings

  property var output: ({})

  function setting(name, fallback) {
    var value = settings ? settings[name] : undefined
    return value === undefined || value === null ? fallback : value
  }

  // First class of the output that has a color configured.
  function classColor(klass) {
    var colors = setting("colors", {})
    var classes = Array.isArray(klass) ? klass : [klass]
    for (var i = 0; i < classes.length; i++) {
      if (colors[classes[i]]) return colors[classes[i]]
    }
    return ""
  }

  readonly property string color: classColor(output.class || "")

  implicitWidth: button.implicitWidth
  implicitHeight: bar ? bar.barSize : 26

  WidgetButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: root.output.text || ""
    tooltipText: root.output.tooltip || ""
    foreground: root.color !== "" ? root.color : (root.bar ? root.bar.barForeground : "white")
    onPressed: function(button) {
      var command = ""
      if (button === Qt.RightButton)
        command = String(root.setting("onRightClick", ""))
      else if (button === Qt.MiddleButton)
        command = String(root.setting("onMiddleClick", ""))
      else
        command = String(root.setting("onClick", ""))
      if (command && root.bar) root.bar.run(command)
    }
  }

  // WidgetButton has no bold switch, so set it on its label directly.
  Component.onCompleted: {
    for (var i = 0; i < button.children.length; i++) {
      var child = button.children[i]
      if (child.font !== undefined) child.font.bold = root.setting("bold", false) === true
    }
  }

  Process {
    id: proc
    command: ["bash", "-lc", String(root.setting("exec", ""))]
    stdout: StdioCollector {
      waitForEnd: true
      onStreamFinished: {
        try {
          root.output = JSON.parse(text)
        } catch (e) {
          root.output = { text: String(text || "").trim() }
        }
      }
    }
  }

  Timer {
    interval: Math.max(1, Number(root.setting("interval", 5))) * 1000
    repeat: true
    running: String(root.setting("exec", "")) !== ""
    triggeredOnStart: true
    onTriggered: if (!proc.running) proc.running = true
  }
}
