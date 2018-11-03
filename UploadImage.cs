using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

public class UploadImage : MonoBehaviour {

    string URL = "https://us-central1-ashra-blood.cloudfunctions.net/handle_test";

    public InputField inputName;

    void Awake() {
        inputName = GameObject.Find ("InputField").GetComponent<InputField> ();

        //ClickRegister();
    }

    public void ClickRegister(){
        StartCoroutine(UploadPNG());
    }

    IEnumerator UploadPNG()
    {
        // We should only read the screen after all rendering is complete
        yield return new WaitForEndOfFrame();

        // Create a texture the size of the screen, RGB24 format
        int width = Screen.width;
        int height = Screen.height;
        var tex = new Texture2D(width, height, TextureFormat.RGB24, false);

        // Read screen contents into the texture
        tex.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        tex.Apply();

        // Encode texture into PNG
        byte[] bytes = tex.EncodeToPNG();
        Destroy(tex);

        // Create a Web Form
        WWWForm form = new WWWForm();
//        form.AddField("frameCount", Time.frameCount.ToString());
        form.AddBinaryData("fileUpload", bytes, "screenShot.png", "image/png");
        form.AddField("studentName", inputName.text);

        // Upload to a cgi script
        using (var w = UnityWebRequest.Post(URL, form))
        {
            yield return w.SendWebRequest();
            if (w.isNetworkError || w.isHttpError)
            {
                Debug.Log(w.error);
            }
            else
            {
                Debug.Log("Finished Uploading Screenshot");
            }
        }
    }
}
