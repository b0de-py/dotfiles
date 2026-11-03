import QtQuick
import Quickshell.Io
import qs.Ui

// Command module que pinta só o número do dia do mês (o primeiro número do
// texto, ex.: "03 Nov, Tue"). Settings em shell.json:
//   exec (JSON {text, tooltip} ou texto puro), interval (s), dayColor "#rrggbb", onClick
Item {
  id: root

  property var bar
  property string moduleName
  property var settings

  property string output: ""
  property string tooltip: ""

  function setting(name, fallback) {
    var value = settings ? settings[name] : undefined
    return value === undefined || value === null ? fallback : value
  }

  readonly property string rich: {
    var color = String(setting("dayColor", ""))
    var escaped = output.replace(/&/g, "&amp;").replace(/</g, "&lt;")
    if (color === "") return escaped
    return escaped.replace(/^(\s*\d+)/, "<font color=\"" + color + "\">$1</font>")
  }

  implicitWidth: button.implicitWidth
  implicitHeight: bar ? bar.barSize : 26

  WidgetButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: root.output
    tooltipText: root.tooltip
    labelVisible: false
    onPressed: function(b) {
      var command = String(root.setting("onClick", ""))
      if (b === Qt.LeftButton && command && root.bar) root.bar.run(command)
    }

    Text {
      anchors.centerIn: parent
      textFormat: Text.RichText
      text: root.rich
      color: root.bar ? root.bar.barForeground : "white"
      font.family: button.fontFamily
      font.pixelSize: button.fontSize
      renderType: Text.NativeRendering
    }
  }

  Process {
    id: proc
    command: ["bash", "-lc", String(root.setting("exec", ""))]
    stdout: StdioCollector {
      waitForEnd: true
      onStreamFinished: {
        try {
          var parsed = JSON.parse(text)
          root.output = String(parsed.text || "")
          root.tooltip = String(parsed.tooltip || "")
        } catch (e) {
          root.output = String(text || "").trim()
        }
      }
    }
  }

  Timer {
    interval: Math.max(1, Number(root.setting("interval", 60))) * 1000
    repeat: true
    running: String(root.setting("exec", "")) !== ""
    triggeredOnStart: true
    onTriggered: if (!proc.running) proc.running = true
  }
}
