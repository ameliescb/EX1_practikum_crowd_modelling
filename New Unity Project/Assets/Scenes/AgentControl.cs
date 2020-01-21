using UnityStandardAssets.Characters.ThirdPerson;
using UnityEngine;
using UnityEngine.AI;

public class AgentControl : MonoBehaviour
{
    public Camera cam;
    NavMeshAgent agent;

    public ThirdPersonCharacter character;

    private void Start()
    {
        agent = this.GetComponent<NavMeshAgent>();
        //character = this.GetComponent<ThirdPersonCharacter>();
        agent.updateRotation = false;
    }

    void Update()
    {
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
        if (agent.remainingDistance > agent.stoppingDistance)
            character.Move(agent.desiredVelocity, false, false);
        else
            character.Move(Vector3.zero, false, false);
    }
}
