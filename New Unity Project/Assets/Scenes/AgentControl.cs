using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class AgentControl : MonoBehaviour
{
    public Transform home;
    public Camera cam;
    NavMeshAgent agent;
   

    void Update()
    {
        agent = this.GetComponent<NavMeshAgent>();
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

    public void BeginSimulation() {
        agent = this.GetComponent<NavMeshAgent>();
        Debug.Log("begin simulation clicked") ;
    } 

    public void SpeedChange(string newSpeed) {
         Debug.Log("speed has been changed : ") ;
         Debug.Log(newSpeed) ;
   } 

   public void pedNumChange(string pedNum) {
         Debug.Log("number of pedestrians has been changed : ") ;
         Debug.Log(pedNum) ;
   } 
}
