using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SpawnObject : MonoBehaviour
{
    public GameObject agent;
    public Vector3 center;
    public Vector3 size;

    public BeginSimulation bs;
    bool once = true;
    
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        if (once)
        {
            if (bs.trigger)
            {
            triggerSpawn(int.Parse(bs.ped_amount));
            this.once = false;
            }
        }
    }

    public void SpawnPedo()
    {
        Vector3 pos = center + new Vector3(Random.Range(-size.x / 2, size.x / 2), Random.Range(-size.y / 2, size.y / 2), Random.Range(-size.z / 2, size.z / 2));
        agent.GetComponent<UnityEngine.AI.NavMeshAgent>().speed = float.Parse(bs.speed);
        Instantiate(agent, pos, Quaternion.identity);
    }

    void OnDrawGizmosSelected()
    {
        Gizmos.color = new Color(1,0,0,0.5f);
        Gizmos.DrawCube(center, size);
    }

    public void triggerSpawn(int amount)
    {
        int i = 0;
        while (i < amount)
        {
            SpawnPedo();
            i++;
        }
    }
}
