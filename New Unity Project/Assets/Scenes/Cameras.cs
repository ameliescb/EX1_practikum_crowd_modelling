using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Cameras : MonoBehaviour
{

    public Camera cam1;
    public Camera cam2;
    public Camera cam3;
    public bool[] enable = new bool[3];
    public int clic = 0;

    // Start is called before the first frame update
    void Start()
    {
        enable[0] = true;
        enable[1] = false;
        enable[2] = false;

        cam1.enabled = true;
        cam2.enabled = false;
        cam3.enabled = false;
    }

    // Update is called once per frame
    void Update()
    {
        bool save = cam3.enabled;
        if (Input.GetKeyDown(KeyCode.C))
        {
            if (cam2.enabled == true)
            {
                cam3.enabled = true;
            }
            else
            {
                cam3.enabled = false;
            }

            if (cam1.enabled == true)
            {
                cam2.enabled = true;
            }
            else
            {
                cam2.enabled = false;
            }
            if (save == true)
            {
                cam1.enabled = true;
            }
            else
            {
                cam1.enabled = false;
            }

            Debug.Log(cam1.enabled);
            cam1.gameObject.SetActive(cam1.enabled);
            cam2.gameObject.SetActive(cam2.enabled);
            cam3.gameObject.SetActive(cam3.enabled);

        }
    }
}
