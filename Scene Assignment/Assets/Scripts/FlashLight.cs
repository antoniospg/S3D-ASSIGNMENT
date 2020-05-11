using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FlashLight : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        var light = GetComponent<Light>();

        //turn on and off FlashLight
        if(Input.GetKeyDown(KeyCode.Mouse1)){
          if(light.enabled == false) light.enabled = true;
          else light.enabled = false;
        }
    }
}
