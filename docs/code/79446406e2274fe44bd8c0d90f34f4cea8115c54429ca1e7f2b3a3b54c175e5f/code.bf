using System;
using System.Net;
using System.Collections;

namespace IDE.Debug
{
    class HttpServer
    {
        TcpListener mListener;
        List<HttpConnection> mConnections = new List<HttpConnection>(); 
        public bool mKeepGoing = true;

        public ~this()
        {
            delete mConnections;
        }

        public void Listen(int32 port)
        {
            mListener = new TcpListener(IPAddress.Parse("127.0.0.1"), port);
            mListener.Start();

            while (mKeepGoing)
            {
                Socket socket = mListener.AcceptSocket();
                HttpConnection connection = new HttpConnection(socket);
                mConnections.Add(connection);
            }
        }
    }
}