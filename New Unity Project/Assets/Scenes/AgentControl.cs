using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class AgentControl : MonoBehaviour
{
    public Transform home;
    public Camera cam;
    NavMeshAgent agent;
    
    // Start is called before the first frame update
  //  void Start()
   // {
        
     //   agent.SetDestination(home.position);
      //  agent.speed = 50 ; 
   // }

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
}
