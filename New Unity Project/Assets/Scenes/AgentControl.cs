using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;
using System ; 

public class AgentControl : MonoBehaviour
{
    public Transform home;
    public Camera cam;
    NavMeshAgent agent;
    int speed = 0; 
    int pedNum = 0; 



    void Update()
    {
        agent = this.GetComponent<NavMeshAgent>();
      //  speedInput.ActivateInputField ();
        if (Input.GetMouseButtonDown(0))
        {
           Ray ray = cam.ScreenPointToRay(Input.mousePosition);
           RaycastHit hit ;

           if (Physics.Raycast(ray,out hit)) 
           {
               // move the agent
               agent.SetDestination(hit.point) ; 
           }
        }


    }

    int getSpeed() {
        return this.speed ;
    }

    int getPedNum() {
        return this.pedNum ;
    }

    public void BeginSimulation() {
        // start simulation using speed and pednum 
    } 

    public void SpeedChange(string newSpeed) {
        this.speed = int.Parse(newSpeed) ;
   } 

   public void pedNumChange(string newPedNum) {

       this.pedNum = int.Parse(newPedNum) ;


   } 
}
