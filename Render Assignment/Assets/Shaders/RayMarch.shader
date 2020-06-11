Shader "Unlit/RayMarch"
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

	    #define MX_STEPS 100
            #define MX_DIST 100
	    #define SURF_DIST 1e-4
      #define pi 3.14159265

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


	  float getDist(float3 p){
		    float3 x = length(p);
		    return x -.5;
	   }


	    float RayMarch(float3 ro, float3 rd){
		float distOrigin = 0 ;
		float distScene;
		for(int i =0; i< MX_STEPS; i++){
		     float3 p = ro + distOrigin*rd;
		     distScene = getDist(p);
		     distOrigin += distScene;
		     if(distOrigin < SURF_DIST || distOrigin > MX_DIST) break;
		}

		return distOrigin;
	    }

	    float3 getNormal(float3 p){
		float2 e = float2(1e-2,0);
		float3 n = getDist(p) - float3(getDist(p+e.xyy), getDist(p+e.yxy), getDist(p+e.yyx));
		return normalize(n);
	    }

            fixed4 frag (v2f i) : SV_Target
            {
		float2 uv = i.uv -.5;
		float3 ro = i.ro;
		float3 rd = normalize(i.hitPos - ro);
		float d = RayMarch(ro, rd);

                // sample the texture
                fixed4 col = 0;

		if(d < MX_DIST){
		    float3 p = ro +rd * d;
		    //float3 n = getNormal(p);
		    col = fixed4(1,1,1,1);
		}
		else discard;

                // apply fog
                UNITY_APPLY_FOG(i.fogCoord, col);
                return col;
            }
            ENDCG
        }
    }
}
