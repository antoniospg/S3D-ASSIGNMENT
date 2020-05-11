using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GlowTrig : MonoBehaviour
{
    bool first = true;

    //trigged when player enters AreaTrigger
    void OnTriggerEnter(Collider other){
      if(first) Burning.instance.count = 0;
      first = false;
    }
}
