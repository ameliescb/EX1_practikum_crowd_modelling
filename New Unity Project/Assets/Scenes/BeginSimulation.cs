using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class BeginSimulation : MonoBehaviour
{

    public string speed;
    public string ped_amount;
    public Color red = Color.red;
    public Camera cm;

    public GameObject speedInput;
    public GameObject ped_amountInput;

    public bool trigger = false;

    // Start is called before the first frame update
    public void getSpeed()
    {
        this.speed = speedInput.GetComponent<Text>().text;
        Debug.Log(this.speed);
    }

    public void getPedNum()
    {
        this.ped_amount = ped_amountInput.GetComponent<Text>().text;
        Debug.Log(this.ped_amount);
    }

    public void simulate()
    {
        cm.backgroundColor = red;
        getSpeed();
        getPedNum();
        trigger = true;
    }

    public void setTriggerFalse()
    {
        this.trigger = false;
    }
}
