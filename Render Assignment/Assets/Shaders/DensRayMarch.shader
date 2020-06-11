﻿Shader "Unlit/DensRayMarch"
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
//-----------------------------------------------------------------------------
// Maths utils
//-----------------------------------------------------------------------------
float3x3 m = float3x3( 0.00,  0.80,  0.60,
              -0.80,  0.36, -0.48,
              -0.60, -0.48,  0.64 );
float hash( float n )
{
    return frac(sin(n)*43758.5453);
}

float noise( in float3 x )
{
    float3 p = floor(x);
    float3 f = frac(x);

    f = f*f*(3.0-2.0*f);

    float n = p.x + p.y*57.0 + 113.0*p.z;

    float res = lerp(lerp(lerp( hash(n+  0.0), hash(n+  1.0),f.x),
                        lerp( hash(n+ 57.0), hash(n+ 58.0),f.x),f.y),
                    lerp(lerp( hash(n+113.0), hash(n+114.0),f.x),
                        lerp( hash(n+170.0), hash(n+171.0),f.x),f.y),f.z);
    return res;
}

float fbm( float3 p )
{
    float f;
    f  = 0.5000*noise( p ); p = mul(m,p)*2.02;
    f += 0.2500*noise( p ); p = mul(m,p)*2.03;
    f += 0.1250*noise( p );
    return f;
}


//-----------------------------------------------------------------------------
// Main functions
//-----------------------------------------------------------------------------
float scene(float3 p)
{
	return .1-length(p)*.05+fbm(p*.3);
}

fixed4 frag (v2f i) : SV_Target
{
	float2 q = i.uv;
    float2 v = i.hitPos;

	#if 0

    #else
	float2 mo = float2(_Time.y*.1,cos(_Time.y*.25)*3.);
	#endif

    // camera by iq
    float3 org = 25.0*normalize(float3(cos(2.75-3.0*mo.x), 0.7-1.0*(mo.y-1.0), sin(2.75-3.0*mo.x)));
	float3 ta = float3(0.0, 1.0, 0.0);
    float3 ww = normalize( ta - org);
    float3 uu = normalize(cross( float3(0.0,1.0,0.0), ww ));
    float3 vv = normalize(cross(ww,uu));
    float3 dir = normalize( v.x*uu + v.y*vv + 1.5*ww );
	float4 color=float4(.0, .0, .0, .0);



	const int nbSample = 64;
	const int nbSampleLight = 6;

	float zMax         = 40.;
	float step         = zMax/float(nbSample);
	float zMaxl         = 20.;
	float stepl         = zMaxl/float(nbSampleLight);
    float3 p             = org;
    float T            = 1.;
    float absorption   = 100.;
	float3 sun_direction = normalize( float3(1.,.0,.0) );

	for(int i=0; i<nbSample; i++)
	{
		float density = scene(p);
		if(density>0.)
		{
			float tmp = density / float(nbSample);
			T *= 1. -tmp * absorption;
			if( T <= 0.01)
				break;


			 //Light scattering
			float Tl = 1.0;
			for(int j=0; j<nbSampleLight; j++)
			{
				float densityLight = scene( p + normalize(sun_direction)*float(j)*stepl);
				if(densityLight>0.)
                	Tl *= 1. - densityLight * absorption/float(nbSample);
                if (Tl <= 0.01)
                    break;
			}

			//Add ambiant + light scattering color
			color += float4(1., 1., 1., 1.)*50.*tmp*T +  float4(1.,.7,.4,1.)*80.*tmp*T*Tl;
		}
		p += dir*step;
	}
    if(color.x < 0.1 && color.y < 0.1 && color.z < 0.1) discard;
    return color;

}

/*
            fixed4 frag (v2f i) : SV_Target
            {
              float2 uv = i.uv -.5;
              float3 ro = i.hitPos;
              float3 rd = normalize(i.hitPos - ro);
                // sample the texture
                float3 col = volumetricTrace(ro, rd);
                if(col.x == 0 && col.y ==0 && col.z ==0) discard;
                // apply fog
                UNITY_APPLY_FOG(i.fogCoord, col);
                return float4(col,1.0);
            }
            */
            ENDCG
        }
    }
}
