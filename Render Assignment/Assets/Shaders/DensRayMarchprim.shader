Shader "Unlit/DensRayMarchprim"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            // make fog work
            #pragma multi_compile_fog

            #include "UnityCG.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                UNITY_FOG_COORDS(1)
                float4 vertex : SV_POSITION;
                float3 ro : TEXCOORD2;
                  float3 hitPos : TEXCOORD3;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;

            v2f vert (appdata v)
            {
              v2f o;
              o.vertex = UnityObjectToClipPos(v.vertex);
              o.uv = TRANSFORM_TEX(v.uv, _MainTex);
              o.ro = mul(unity_WorldToObject,float4(_WorldSpaceCameraPos,1));
              o.hitPos = v.vertex;
              UNITY_TRANSFER_FOG(o,o.vertex);
              return o;
            }
////////////////////////////////////////////////////////////
float rand(float3 p) {
    return frac(sin(dot(p, float3(12.345, 67.89, 412.12))) * 42123.45) * 2.0 - 1.0;
}

// A perlin noise function. Since we are not using textures, we am gonna sample 8 corners of a cube.
float perlin(float3 p) {
    float3 u = floor(p);
    float3 v = frac(p);
    float3 s = smoothstep(0.0, 1.0, v);

    float a = rand(u);
    float b = rand(u + float3(1.0, 0.0, 0.0));
    float c = rand(u + float3(0.0, 1.0, 0.0));
    float d = rand(u + float3(1.0, 1.0, 0.0));
    float e = rand(u + float3(0.0, 0.0, 1.0));
    float f = rand(u + float3(1.0, 0.0, 1.0));
    float g = rand(u + float3(0.0, 1.0, 1.0));
    float h = rand(u + float3(1.0, 1.0, 1.0));

    return lerp(lerp(lerp(a, b, s.x), lerp(c, d, s.x), s.y),
               lerp(lerp(e, f, s.x), lerp(g, h, s.x), s.y),
               s.z);
}

// The fbm function. iq unrolled the loop, so I am doing it too.
// If you wonder what fbm is, check this out: https://thebookofshaders.com/13/
float fbm(float3 p) {
    float3 off = float3(0.0, 0.1, 1.0) * _Time.y;
    float3 q = p - off;

    // fbm
    float f = 0.5 * perlin(q); q *= 2.0;
    f += 0.25 * perlin(q); q *= 2.0;
    f += 0.125 * perlin(q); q *= 2.0;
    f += 0.06250 * perlin(q); q *= 2.0;
    f += 0.03125 * perlin(q);
    return clamp(exp(0.5 - length(p)*5), 0.0, 1.0);
}

// volmetric raymarching, which is kinda like the core algorithm.
// I ripped lighting calculations and other stuffs off, so this is bare bones raymarching
float3 volumetricTrace(float3 ro, float3 rd) {
    // at first there's no depth
    float depth = 0.0;

    // and the color's black
    float4 sumColor = float4(0.0,0.0,0.0,0.0);

    // then we begin to march
    for (int i = 0; i < 100; i++) {
        float3 p = ro + depth * rd;

        // and we get the cloud density at said position
        float density = fbm(p);
        // if there is an unignorable amount of density (the cloud is thick enough) then
        if (density > 1e-3) {
            // we estimate the color with density (the thicker, the whiter)
            float4 color = float4(lerp(float3(0.0,0.0,0.0), float3(1.0,1.0,1.0), density), density);
            // and we multiply it by a factor so it makes the clouds softer
            color.w *= 0.4;
            color.rgb *= color.w;
            // sumColor.w will rise steadily, which stands for when the ray hits thick enough cloud,
            // its color won't change anymore
            sumColor += color * (1.0 - sumColor.a);
        }
        // we march forward
        depth += max(0.05, 0.02 * depth);
    }
    return clamp(sumColor.rgb, 0.0, 1.0);
}

            fixed4 frag (v2f i) : SV_Target
            {
              float2 uv = i.uv;
              float3 ro = i.ro;
              float3 rd = normalize(i.hitPos - ro);
                // sample the texture
                float3 col = volumetricTrace(ro, rd);
                if(col.x <.1 && col.y<.1 && col.z <.1) discard;
                // apply fog
                UNITY_APPLY_FOG(i.fogCoord, col);
                return float4(col,1.0);
            }
            ENDCG
        }
    }
}
