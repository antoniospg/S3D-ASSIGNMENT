using System;
using UnityEngine;
using UnityEngine.Rendering.PostProcessing;

[Serializable]
[PostProcess(typeof(PsRenderer), PostProcessEvent.AfterStack, "Custom/Invert")]

public sealed class PsProcess : PostProcessEffectSettings {

  [Range(0f, 1f), Tooltip("Grayscale effect intensity.")]
  public FloatParameter blend = new FloatParameter { value = 0.5f };
}

public sealed class PsRenderer : PostProcessEffectRenderer<PsProcess> {

  public override void Render(PostProcessRenderContext context) {
      var sheet = context.propertySheets.Get(Shader.Find("Unlit/PosProcess"));
      //sheet.properties.SetFloat("_Blend", settings.blend);
      context.command.BlitFullscreenTriangle(context.source, context.destination, sheet, 0);
    }
}
