using UnityEngine;
using UnityEngine.EventSystems;
using DomesticRefrigerator.Core;

namespace DomesticRefrigerator.Interaction
{
    public class ComponentSelector : MonoBehaviour
    {
        [SerializeField] private Camera interactionCamera;
        [SerializeField] private LayerMask selectableLayer = ~0;

        private void Start()
        {
            if (interactionCamera == null) interactionCamera = Camera.main;
        }

        private void Update()
        {
            // Do not raycast if pointer is over UI elements
            if (EventSystem.current != null && EventSystem.current.IsPointerOverGameObject())
                return;

            if (Input.GetMouseButtonDown(0))
            {
                HandlePointerSelection(Input.mousePosition);
            }
            else if (Input.touchCount > 0 && Input.GetTouch(0).phase == TouchPhase.Began)
            {
                if (!EventSystem.current.IsPointerOverGameObject(Input.GetTouch(0).fingerId))
                {
                    HandlePointerSelection(Input.GetTouch(0).position);
                }
            }
        }

        private void HandlePointerSelection(Vector2 screenPos)
        {
            if (interactionCamera == null) return;

            Ray ray = interactionCamera.ScreenPointToRay(screenPos);
            if (Physics.Raycast(ray, out RaycastHit hit, 100f, selectableLayer))
            {
                // Trace up to find top-level component group under Domestic_Refrigerator
                Transform current = hit.transform;
                Transform refrigRoot = RefrigeratorController.Instance ? RefrigeratorController.Instance.transform : null;

                if (refrigRoot != null)
                {
                    while (current != null && current.parent != refrigRoot && current.parent != null)
                    {
                        current = current.parent;
                    }

                    if (current != null && current.parent == refrigRoot)
                    {
                        string compId = current.name;
                        RefrigeratorController.Instance.SelectComponent(compId);
                    }
                }
            }
        }
    }
}
