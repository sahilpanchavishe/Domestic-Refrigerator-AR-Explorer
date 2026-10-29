using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace DomesticRefrigerator.AR
{
    public class ARController : MonoBehaviour
    {
        [Header("AR Placement Target")]
        [SerializeField] private GameObject refrigeratorPrefab;
        [SerializeField] private Transform arPlacementAnchor;

        [Header("UI Feedback")]
        [SerializeField] private Text arStatusText;
        [SerializeField] private GameObject permissionPromptPanel;
        [SerializeField] private GameObject placementReticle;
        [SerializeField] private Button startARButton;
        [SerializeField] private Button resetPlacementButton;

        [Header("Camera Overlay Fallback")]
        [SerializeField] private RawImage cameraBackgroundFeed;
        [SerializeField] private bool useFallbackWebcam = false;

        private WebCamTexture webCamTexture;
        private GameObject spawnedRefrigerator;
        private bool isPlaced = false;

        private void Start()
        {
            if (permissionPromptPanel) permissionPromptPanel.SetActive(true);
            if (placementReticle) placementReticle.SetActive(false);

            if (startARButton) startARButton.onClick.AddListener(RequestCameraAndStartAR);
            if (resetPlacementButton) resetPlacementButton.onClick.AddListener(ResetPlacement);
        }

        public void RequestCameraAndStartAR()
        {
            StartCoroutine(InitializeCameraRoutine());
        }

        private IEnumerator InitializeCameraRoutine()
        {
            if (arStatusText) arStatusText.text = "Requesting camera permissions...";

#if UNITY_ANDROID && !UNITY_EDITOR
            if (!UnityEngine.Android.Permission.HasUserAuthorizedPermission(UnityEngine.Android.Permission.Camera))
            {
                UnityEngine.Android.Permission.RequestUserPermission(UnityEngine.Android.Permission.Camera);
                yield return new WaitForSeconds(1.0f);
            }

            if (!UnityEngine.Android.Permission.HasUserAuthorizedPermission(UnityEngine.Android.Permission.Camera))
            {
                if (arStatusText) arStatusText.text = "Camera permission denied. Please enable in Settings to use AR mode.";
                yield break;
            }
#endif

            if (permissionPromptPanel) permissionPromptPanel.SetActive(false);
            if (arStatusText) arStatusText.text = "Scanning surroundings for horizontal surfaces...";

            // Start webcam feed for device camera overlay fallback if AR Foundation plane is unsupported
            if (WebCamTexture.devices.Length > 0 && cameraBackgroundFeed != null)
            {
                string backCamName = "";
                foreach (var device in WebCamTexture.devices)
                {
                    if (!device.isFrontFacing)
                    {
                        backCamName = device.name;
                        break;
                    }
                }
                if (string.IsNullOrEmpty(backCamName)) backCamName = WebCamTexture.devices[0].name;

                webCamTexture = new WebCamTexture(backCamName, 1920, 1080, 30);
                cameraBackgroundFeed.texture = webCamTexture;
                webCamTexture.Play();
            }

            if (placementReticle) placementReticle.SetActive(true);
            yield return null;
        }

        private void Update()
        {
            if (!isPlaced && placementReticle != null && placementReticle.activeSelf)
            {
                // Touch tap or click to place model
                if (Input.GetMouseButtonDown(0) || (Input.touchCount > 0 && Input.GetTouch(0).phase == TouchPhase.Began))
                {
                    PlaceRefrigerator();
                }
            }

            // Pinch to scale or 2-finger rotate when placed
            if (isPlaced && spawnedRefrigerator != null)
            {
                HandleGestures();
            }
        }

        private void PlaceRefrigerator()
        {
            if (refrigeratorPrefab == null) return;

            Vector3 spawnPos = arPlacementAnchor != null ? arPlacementAnchor.position : new Vector3(0, -0.4f, 1.8f);
            Quaternion spawnRot = Quaternion.Euler(0, 180f, 0);

            if (spawnedRefrigerator == null)
            {
                spawnedRefrigerator = Instantiate(refrigeratorPrefab, spawnPos, spawnRot);
            }
            else
            {
                spawnedRefrigerator.transform.position = spawnPos;
                spawnedRefrigerator.transform.rotation = spawnRot;
                spawnedRefrigerator.SetActive(true);
            }

            isPlaced = true;
            if (placementReticle) placementReticle.SetActive(false);
            if (arStatusText) arStatusText.text = "Refrigerator placed in your room. Tap parts or open doors to explore.";
        }

        private void HandleGestures()
        {
            // Touch gesture for scaling and rotation
            if (Input.touchCount == 2)
            {
                Touch t0 = Input.GetTouch(0);
                Touch t1 = Input.GetTouch(1);

                // Pinch zoom
                Vector2 prev0 = t0.position - t0.deltaPosition;
                Vector2 prev1 = t1.position - t1.deltaPosition;
                float prevDist = (prev0 - prev1).magnitude;
                float curDist = (t0.position - t1.position).magnitude;
                float scaleFactor = curDist / prevDist;

                Vector3 curScale = spawnedRefrigerator.transform.localScale;
                curScale *= scaleFactor;
                curScale = Vector3.ClampMagnitude(curScale, 2.0f);
                if (curScale.magnitude > 0.1f)
                    spawnedRefrigerator.transform.localScale = curScale;

                // Two-finger twist rotation
                float prevAngle = Mathf.Atan2(prev1.y - prev0.y, prev1.x - prev0.x) * Mathf.Rad2Deg;
                float curAngle = Mathf.Atan2(t1.y - t0.y, t1.x - t0.x) * Mathf.Rad2Deg;
                float deltaAngle = Mathf.DeltaAngle(prevAngle, curAngle);

                spawnedRefrigerator.transform.Rotate(0, -deltaAngle, 0, Space.World);
            }
        }

        public void ResetPlacement()
        {
            isPlaced = false;
            if (spawnedRefrigerator) spawnedRefrigerator.SetActive(false);
            if (placementReticle) placementReticle.SetActive(true);
            if (arStatusText) arStatusText.text = "Tap on a table or floor to place the refrigerator.";
        }

        private void OnDestroy()
        {
            if (webCamTexture != null && webCamTexture.isPlaying)
            {
                webCamTexture.Stop();
            }
        }
    }
}
