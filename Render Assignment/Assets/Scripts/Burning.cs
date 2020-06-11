using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine.Rendering;

public class Burning : MonoBehaviour {

    public static Burning instance;

    List<KeyValuePair<Vector3, float>> facesList = new List<KeyValuePair<Vector3, float>>();
    List<int> currentFaces = new List<int>();
    Mesh clonedMesh;
    Mesh glMesh;

    public int count;

    public GameObject glow;

    void Start() {

        //get meshes parameters
        var meshFilter = GetComponent<MeshFilter>();
        var sourceMesh = meshFilter.sharedMesh;
        var triangles = sourceMesh.GetTriangles(0);

        //assign to faceList the y values of first vertices of each face
        for(int i =0; i< triangles.Length/3; i++){

        facesList.Add(new KeyValuePair<Vector3, float>(new Vector3(triangles[3*i], triangles[3*i+1],
                                                        triangles[3*i+2]), sourceMesh.vertices[triangles[3*i]].y));
        }

        //sort the list
        facesList.Sort(Compare2);

        //create the new mesh for the ParticleSystem
        clonedMesh = new Mesh();
        clonedMesh.name = "clone";
        clonedMesh.vertices = sourceMesh.vertices;
        clonedMesh.normals = sourceMesh.normals;
        clonedMesh.uv = sourceMesh.uv;

        //glowing mesh
        glMesh = new Mesh();
        glMesh = glow.GetComponent<MeshFilter>().mesh;
        glMesh.vertices = clonedMesh.vertices;
        glMesh.normals = clonedMesh.normals;
        glMesh.uv = clonedMesh.uv;

        //trigger params
        instance = this;
        count = -1;
    }

    void Update(){

      //if the effect was trigged
      if (count != -1){

        var sourceMesh = GetComponent<MeshFilter>().sharedMesh;
        var triangles = sourceMesh.GetTriangles(0);
        float fire = 1;

        if(count < triangles.Length/3){

          //increment particle size each iteraction
          if(count <= 300){
            fire = count*0.005f;
          }
          else fire = 1.5f;

          //add the current face each frame
          currentFaces.Add((int)facesList[count].Key.x);
          currentFaces.Add((int)facesList[count].Key.y);
          currentFaces.Add((int)facesList[count].Key.z);

          count++;
        }

        //assign to glow mesh
        glMesh.vertices = sourceMesh.vertices;
        glMesh.triangles = currentFaces.ToArray();
        glMesh.RecalculateBounds();

        //asign the values to the clonedmesh
        clonedMesh.vertices = sourceMesh.vertices;
        clonedMesh.triangles = currentFaces.ToArray();
        clonedMesh.RecalculateBounds();

        //assign to the ParticleSystem
        ParticleSystem ps = GetComponent<ParticleSystem>();
        var sh = ps.shape;
        sh.enabled = true;
        sh.shapeType = ParticleSystemShapeType.Mesh;
        sh.mesh = clonedMesh;
        var main = ps.main;
        main.startSize = fire;

      }
    }

    static int Compare2(KeyValuePair<Vector3, float> a, KeyValuePair<Vector3, float> b){
        return a.Value.CompareTo(b.Value);
    }

    float calcArea(Vector3[] vertices, Vector3 face){
      var matrix  = new Matrix4x4();
      int a = (int)face.x;
      int b = (int)face.y;
      int c = (int)face.z;

      matrix.SetRow(0, new Vector4(1,0,0,0));
      matrix.SetRow(1, new Vector4(1,vertices[a].x, vertices[a].y, vertices[a].z));
      matrix.SetRow(2, new Vector4(1,vertices[b].x, vertices[b].y, vertices[b].z));
      matrix.SetRow(3, new Vector4(1,vertices[c].x, vertices[c].y, vertices[c].z));
      return Math.Abs(matrix.determinant);
    }
}
