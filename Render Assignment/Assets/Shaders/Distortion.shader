Shader "Custom/Unlit/Distortion"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
	_Noise("Noise", 2D) = "white" {}
        _Strength("Distort Strength", float) = 1.0
        _Speed("Distort Speed", float) = 1.0
	_StrengthFilter("Strength Filter", 2D) = "white" {}
    }
    SubShader
    {
        Tags 
	{
 	    "Queue" = "Transparent-200"
            "DisableBatching" = "True"
	    "IgnoreProjector"="True"
	    "RenderType"="Transparent"
	}
        LOD 100


        Pass
        {
	    ZTest Always

	    CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            // make fog work
            #pragma multi_compile_fog

            #include "UnityCG.cginc"

	    // Properties
            sampler2D _Noise;
            sampler2D _StrengthFilter;
            sampler2D _BackgroundTexture;
            float     _Strength;
            float     _Speed;


            struct appdata
            {
                float4 vertex : POSITION;
                float3 uv : TEXCOORD0;
            };

            struct v2f
            {
                float4 uv : TEXCOORD0;
                UNITY_FOG_COORDS(1)
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;

            v2f vert (appdata v)
            {
                v2f output;
		

		float4 pos = v.vertex;
		// transform origin to view space
		float4 originInViewSpace = mul(UNITY_MATRIX_MV, float4(0, 4, 0, 3));
		// translate view space point by vertex position
		float4 vertInViewSpace = originInViewSpace + float4(pos.x, pos.z, 0, 0);
		// convert from view space to projection space
		pos = mul(UNITY_MATRIX_P, vertInViewSpace);
		output.vertex = pos;

		output.uv = ComputeGrabScreenPos(output.vertex);	
		float noise = tex2Dlod(_Noise, float4(v.uv,0)).rgb;
		float filter = tex2Dlod(_StrengthFilter, float4(v.uv,0)).rgb;
		output.uv.x += cos(noise*_Time.x*_Speed) * _Strength *filter ;
		output.uv.y += sin(noise*_Time.x*_Speed) * _Strength *filter ;	

		return output;
 
            }

	    sampler2D _CameraOpaqueTexture;
            float4 frag (v2f i) : COLOR
            {
               	return tex2Dproj(_CameraOpaqueTexture, i.uv);
            }
            ENDCG
        }
    }
}
