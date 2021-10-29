using UnityEngine;
using System.Collections;

[ExecuteInEditMode]
public class NewBehaviourScript : MonoBehaviour
{
    public Vector3 offset = new Vector3(0, 1, 0);
    Camera cam;
    private Matrix4x4 m;
    public Vector3 eulerAngles;

    void Start()
    {
        cam = GetComponent<Camera>();
        cam.ResetProjectionMatrix();
    }

    void LateUpdate()
    {
        Vector3 camoffset = new Vector3(-offset.x, -offset.y, offset.z);
        Quaternion rotation = Quaternion.Euler(eulerAngles.x, eulerAngles.y, eulerAngles.z);
        Matrix4x4 m = Matrix4x4.TRS(camoffset, rotation, new Vector3(1, 1, -1));
        Debug.Log(cam.name +'\n'+ m.ToString());
        cam.worldToCameraMatrix = m * transform.worldToLocalMatrix;
    }
}