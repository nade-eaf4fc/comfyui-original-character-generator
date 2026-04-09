import { app } from "../../../scripts/app.js";

app.registerExtension({
  name: "comfyui.generate_original_character.preset_sync",
  beforeRegisterNodeDef(nodeType, nodeData) {
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

    function findWidget(node, name) {
      return node.widgets?.find((widget) => widget.name === name) || null;
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

    function applyPreset(node, presetName) {
      const preset = presets[presetName];
      if (!preset) {
        return;
      }

      Object.entries(preset).forEach(([name, value]) => {
        setWidgetValue(node, name, value);
      });

      node.setDirtyCanvas?.(true, true);
      node.graph?.setDirtyCanvas?.(true, true);
    }

    const originalOnNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
      const result = originalOnNodeCreated ? originalOnNodeCreated.apply(this, arguments) : undefined;
      const presetWidget = findWidget(this, "preset");

      if (!presetWidget || presetWidget.__ocPresetHooked) {
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
      return result;
    };
  },
});
