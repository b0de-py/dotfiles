import QtQuick
import Quickshell.Io
import qs.Ui

// AI usage drawer: Claude stays visible, Antigravity slides out on hover,
// mimicking the tray's chevron drawer. Data comes from ai-usagebar.
Item {
  id: root

  property var bar
  property string moduleName
  property var settings

  property bool expanded: false
  property real reveal: expanded ? 1 : 0
  readonly property int interval: settings && settings.interval ? Number(settings.interval) : 300

  implicitWidth: row.implicitWidth
  implicitHeight: bar ? bar.barSize : 26

  Behavior on reveal {
    NumberAnimation { duration: 600; easing.type: Easing.OutCubic }
  }

  HoverHandler {
    onHoveredChanged: root.expanded = hovered
  }

  // Bar renders plain text only, so drop ai-usagebar's Pango markup.
  function parse(raw) {
    var clean = String(raw || "").replace(/<[^>]+>/g, "")
    try {
      return JSON.parse(clean)
    } catch (e) {
      return { text: clean.trim(), tooltip: "", class: "" }
    }
  }

  function urgent(data) {
    var klass = String(data.class || "")
    return klass === "high" || klass === "critical"
  }

  Row {
    id: row
    anchors.verticalCenter: parent.verticalCenter

    BarIconButton {
      bar: root.bar
      text: root.expanded ? "" : ""
      pressable: false
    }

    WidgetButton {
      id: claude
      bar: root.bar
      property var usage: ({})
      text: usage.text || ""
      tooltipText: usage.tooltip || ""
      active: root.urgent(usage)
      onPressed: if (root.bar) root.bar.run("ai-usagebar-tui")
    }

    Item {
      width: antigravity.implicitWidth * root.reveal
      height: root.implicitHeight
      clip: true
      visible: width > 0

      WidgetButton {
        id: antigravity
        bar: root.bar
        property var usage: ({})
        text: usage.text || ""
        tooltipText: usage.tooltip || ""
        active: root.urgent(usage)
        onPressed: if (root.bar) root.bar.run("ai-usagebar-tui")
      }
    }
  }

  Process {
    id: claudeProc
    command: ["bash", "-lc", "ai-usagebar --vendor anthropic --icon '󰚩'"]
    stdout: StdioCollector {
      waitForEnd: true
      onStreamFinished: claude.usage = root.parse(text)
    }
  }

  Process {
    id: antigravityProc
    command: ["bash", "-lc", "ai-usagebar --vendor antigravity --icon '󰘧' --format '{session_pct}% · {session_reset}'"]
    stdout: StdioCollector {
      waitForEnd: true
      onStreamFinished: antigravity.usage = root.parse(text)
    }
  }

  Timer {
    interval: Math.max(30, root.interval) * 1000
    repeat: true
    running: true
    triggeredOnStart: true
    onTriggered: {
      claudeProc.running = true
      antigravityProc.running = true
    }
  }
}
