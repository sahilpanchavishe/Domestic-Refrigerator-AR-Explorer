using UnityEngine;
using UnityEngine.EventSystems;

namespace DomesticRefrigerator.Core
{
    public class OrbitCameraController : MonoBehaviour
    {
        [Header("Target & Distances")]
        [SerializeField] private Transform target;
        [SerializeField] private Vector3 targetOffset = new Vector3(0, 0.95f, 0);
        [SerializeField] private float distance = 2.4f;
        [SerializeField] private float minDistance = 0.8f;
        [SerializeField] private float maxDistance = 4.5f;

        [Header("Speeds")]
        [SerializeField] private float xSpeed = 160f;
        [SerializeField] private float ySpeed = 120f;
        [SerializeField] private float zoomSpeed = 2.5f;
        [SerializeField] private float damping = 6f;

        [Header("Limits")]
        [SerializeField] private float yMinLimit = -20f;
        [SerializeField] private float yMaxLimit = 80f;

        private float currentX = 35f;
        private float currentY = 15f;
        private float targetX = 35f;
        private float targetY = 15f;
        private float targetDistance;

        private Vector3 targetPos;

        private void Start()
        {
            targetDistance = distance;
            targetPos = target != null ? target.position + targetOffset : targetOffset;
            Vector3 angles = transform.eulerAngles;
            currentX = angles.y;
            currentY = angles.x;
            targetX = currentX;
            targetY = currentY;
        }

        private void LateUpdate()
        {
            if (EventSystem.current != null && EventSystem.current.IsPointerOverGameObject())
                return;

            // Mouse orbit
            if (Input.GetMouseButton(0) || Input.GetMouseButton(1))
            {
                targetX += Input.GetAxis("Mouse X") * xSpeed * 0.02f;
                targetY -= Input.GetAxis("Mouse Y") * ySpeed * 0.02f;
                targetY = ClampAngle(targetY, yMinLimit, yMaxLimit);
            }

            // Mouse scroll zoom
            float scroll = Input.GetAxis("Mouse ScrollWheel");
            if (Mathf.Abs(scroll) > 0.001f)
            {
                targetDistance -= scroll * zoomSpeed;
                targetDistance = Mathf.Clamp(targetDistance, minDistance, maxDistance);
            }

            // Touch orbit & pinch zoom
            if (Input.touchCount == 1 && Input.GetTouch(0).phase == TouchPhase.Moved)
            {
                Touch t = Input.GetTouch(0);
                targetX += t.deltaPosition.x * xSpeed * 0.002f;
                targetY -= t.deltaPosition.y * ySpeed * 0.002f;
                targetY = ClampAngle(targetY, yMinLimit, yMaxLimit);
            }
            else if (Input.touchCount == 2)
            {
                Touch t0 = Input.GetTouch(0);
                Touch t1 = Input.GetTouch(1);
                Vector2 prevPos0 = t0.position - t0.deltaPosition;
                Vector2 prevPos1 = t1.position - t1.deltaPosition;

                float prevMag = (prevPos0 - prevPos1).magnitude;
                float currentMag = (t0.position - t1.position).magnitude;
                float diff = currentMag - prevMag;

                targetDistance -= diff * 0.005f * zoomSpeed;
                targetDistance = Mathf.Clamp(targetDistance, minDistance, maxDistance);
            }

            // Smooth interpolation
            currentX = Mathf.Lerp(currentX, targetX, Time.deltaTime * damping);
            currentY = Mathf.Lerp(currentY, targetY, Time.deltaTime * damping);
            distance = Mathf.Lerp(distance, targetDistance, Time.deltaTime * damping);

            Quaternion rotation = Quaternion.Euler(currentY, currentX, 0);
            Vector3 position = rotation * new Vector3(0.0f, 0.0f, -distance) + targetPos;

            transform.rotation = rotation;
            transform.position = position;
        }

        public void SetViewPreset(string preset)
        {
            switch (preset.ToLower())
            {
                case "front":
                    targetX = 0f;
                    targetY = 5f;
                    targetDistance = 2.2f;
                    break;
                case "rear":
                    targetX = 180f;
                    targetY = 10f;
                    targetDistance = 2.2f;
                    break;
                case "interior":
                    targetX = 0f;
                    targetY = 0f;
                    targetDistance = 1.5f;
                    break;
                case "reset":
                default:
                    targetX = 35f;
                    targetY = 15f;
                    targetDistance = 2.4f;
                    break;
            }
        }

        private static float ClampAngle(float angle, float min, float max)
        {
            if (angle < -360F) angle += 360F;
            if (angle > 360F) angle -= 360F;
            return Mathf.Clamp(angle, min, max);
        }
    }
}
