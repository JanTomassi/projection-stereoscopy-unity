using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System;
using UnityEngine;
using System.Threading;

public class CubePos : MonoBehaviour
{
     Thread mThread;
    private string connectionIP = "127.0.0.1";
    private int connectionPort = 25001;
    IPAddress localAdd;
    TcpListener listener;
    TcpClient client;
    public Vector3 receivedPos = Vector3.zero;

    public Vector2 pos1 = Vector2.zero;
    public Vector2 pos2 = Vector2.zero;

    bool running;

    private void Update()
    {
        transform.position = receivedPos; //assigning receivedPos in SendAndReceiveData()
    }

    private void Start()
    {
        ThreadStart ts = new ThreadStart(GetInfo);
        mThread = new Thread(ts);
        mThread.Start();
    }

    void GetInfo()
    {
        localAdd = IPAddress.Parse(connectionIP);
        listener = new TcpListener(IPAddress.Any, connectionPort);
        listener.Start();

        client = listener.AcceptTcpClient();

        running = true;
        while (running)
        {
            SendAndReceiveData();
        }
        listener.Stop();
    }

    void SendAndReceiveData()
    {
        NetworkStream nwStream = client.GetStream();
        byte[] buffer = new byte[client.ReceiveBufferSize];

        byte[] myWriteBuffer = Encoding.UTF8.GetBytes(String.Format("{0} {1} {2} {3}",
                                                                        pos1.x, pos1.y, pos2.x, pos2.y)); //Converting string to byte data
        nwStream.Write(myWriteBuffer, 0, myWriteBuffer.Length); //Sending the data in Bytes to Python

        //---receiving Data from the Host----
        int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize); //Getting data in Bytes from Python
        string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead); //Converting byte data to string

        if (dataReceived != null)
        {
            Debug.Log(dataReceived);
            receivedPos = StringToVector3(dataReceived);
        }
    }

    public static Vector3 StringToVector3(string sVector)
    {

        // split the items
        string[] sArray = sVector.Split(',');

        // store as a Vector3
        Vector3 result = new Vector3(
            (float) double.Parse(sArray[0]),
            (float) double.Parse(sArray[1]),
            (float) double.Parse(sArray[2]));

        return result;
    }
}
