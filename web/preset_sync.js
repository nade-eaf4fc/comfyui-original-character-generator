import { app } from "../../../scripts/app.js";

app.registerExtension({
  name: "comfyui.generate_original_character.preset_sync",
  beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.name === "OC Generator Show Settings") {
      const originalOnNodeCreated = nodeType.prototype.onNodeCreated;
      const originalOnExecuted = nodeType.prototype.onExecuted;

      nodeType.prototype.onNodeCreated = function () {
        const result = originalOnNodeCreated ? originalOnNodeCreated.apply(this, arguments) : undefined;

        if (!this.__ocSettingsSummaryWidget) {
          const widget = this.addWidget("text", "settings_summary", "", () => {}, {
            multiline: true,
          });
          widget.inputEl.readOnly = true;
          widget.inputEl.style.opacity = "0.88";
          widget.inputEl.style.minHeight = "220px";
          this.__ocSettingsSummaryWidget = widget;
          this.size = [Math.max(this.size?.[0] || 320, 360), Math.max(this.size?.[1] || 180, 320)];
        }

        return result;
      };

      nodeType.prototype.onExecuted = function (message) {
        if (typeof originalOnExecuted === "function") {
          originalOnExecuted.apply(this, arguments);
        }

        if (!this.__ocSettingsSummaryWidget) {
          return;
        }

        const summary = Array.isArray(message?.settings_summary)
          ? message.settings_summary[0] || ""
          : "";

        this.__ocSettingsSummaryWidget.value = summary;
        if (this.__ocSettingsSummaryWidget.inputEl) {
          this.__ocSettingsSummaryWidget.inputEl.value = summary;
        }
        this.setDirtyCanvas?.(true, true);
        this.graph?.setDirtyCanvas?.(true, true);
      };

      return;
    }

    if (!["OC Generator Settings", "OC Generator Generate Character Simple"].includes(nodeData.name)) {
      return;
    }

    const presets = {
      Balanced: {
        weight_flat: 0.18,
        weight_small: 0.28,
        weight_medium: 0.26,
        weight_large: 0.18,
        weight_xlarge: 0.1,
        accessory_probability: 0.58,
      },
      Petite: {
        weight_flat: 0.44,
        weight_small: 0.28,
        weight_medium: 0.16,
        weight_large: 0.08,
        weight_xlarge: 0.04,
        accessory_probability: 0.38,
      },
      Curvy: {
        weight_flat: 0.08,
        weight_small: 0.16,
        weight_medium: 0.28,
        weight_large: 0.28,
        weight_xlarge: 0.2,
        accessory_probability: 0.72,
      },
      Statement: {
        weight_flat: 0.04,
        weight_small: 0.1,
        weight_medium: 0.2,
        weight_large: 0.3,
        weight_xlarge: 0.36,
        accessory_probability: 0.86,
      },
    };
    const USER_SETTINGS_PRESET = "User settings";
    const MANUAL_WIDGET_NAMES = [
      "weight_flat",
      "weight_small",
      "weight_medium",
      "weight_large",
      "weight_xlarge",
      "accessory_probability",
    ];

    function findWidget(node, name) {
      return node.widgets?.find((widget) => widget.name === name) || null;
    }

    function relabelWidget(node, name, label) {
      const widget = findWidget(node, name);
      if (!widget) {
        return;
      }

      widget.label = label;
    }

    function setWidgetValue(node, name, value) {
      const widget = findWidget(node, name);
      if (!widget) {
        return;
      }

      widget.value = value;
      if (typeof widget.callback === "function") {
        widget.callback(widget.value);
      }
    }

    function setWidgetEditable(widget, editable) {
      if (!widget) {
        return;
      }

      widget.disabled = !editable;

      if (widget.inputEl) {
        widget.inputEl.disabled = !editable;
        widget.inputEl.readOnly = !editable;
        widget.inputEl.style.opacity = editable ? "1" : "0.6";
        widget.inputEl.style.cursor = editable ? "" : "not-allowed";
      }
    }

    function syncManualWidgetsState(node, presetName) {
      const editable = presetName === USER_SETTINGS_PRESET;

      MANUAL_WIDGET_NAMES.forEach((name) => {
        setWidgetEditable(findWidget(node, name), editable);
      });

      node.setDirtyCanvas?.(true, true);
      node.graph?.setDirtyCanvas?.(true, true);
    }

    function applyPreset(node, presetName) {
      const preset = presets[presetName];
      if (!preset) {
        syncManualWidgetsState(node, presetName);
        return;
      }

      Object.entries(preset).forEach(([name, value]) => {
        setWidgetValue(node, name, value);
      });

      syncManualWidgetsState(node, presetName);
    }

    const originalOnNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
      const result = originalOnNodeCreated ? originalOnNodeCreated.apply(this, arguments) : undefined;
      const presetWidget = findWidget(this, "preset");

      relabelWidget(this, "preset", "preset_profile");
      relabelWidget(this, "fixed_hair_style", "fixed_hair_style");
      relabelWidget(this, "fixed_hair_color", "fixed_hair_color");
      relabelWidget(this, "fixed_eye_color", "fixed_eye_color");
      relabelWidget(this, "fixed_accessory", "fixed_accessory");
      relabelWidget(this, "fixed_bust_size", "fixed_bust_size");

      MANUAL_WIDGET_NAMES.forEach((name) => {
        const widget = findWidget(this, name);
        if (!widget || widget.__ocManualHooked) {
          return;
        }

        const originalCallback = widget.callback;
        widget.callback = (...args) => {
          if (presetWidget && presetWidget.value !== USER_SETTINGS_PRESET) {
            presetWidget.value = USER_SETTINGS_PRESET;
            syncManualWidgetsState(this, USER_SETTINGS_PRESET);
          }
          if (typeof originalCallback === "function") {
            return originalCallback.apply(widget, args);
          }
          return undefined;
        };
        widget.__ocManualHooked = true;
      });

      if (!presetWidget || presetWidget.__ocPresetHooked) {
        if (presetWidget) {
          syncManualWidgetsState(this, presetWidget.value);
        }
        return result;
      }

      const originalCallback = presetWidget.callback;
      presetWidget.callback = (...args) => {
        const nextValue = args[0] ?? presetWidget.value;
        applyPreset(this, nextValue);
        if (typeof originalCallback === "function") {
          return originalCallback.apply(presetWidget, args);
        }
        return undefined;
      };
      presetWidget.__ocPresetHooked = true;
      syncManualWidgetsState(this, presetWidget.value);
      return result;
    };
  },
});
