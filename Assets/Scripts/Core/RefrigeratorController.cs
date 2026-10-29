using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using DomesticRefrigerator.Data;

namespace DomesticRefrigerator.Core
{
    public class RefrigeratorController : MonoBehaviour
    {
        public static RefrigeratorController Instance { get; private set; }

        [Header("Door Hinges")]
        [SerializeField] private Transform leftDoorHinge;
        [SerializeField] private Transform rightDoorHinge;
        [SerializeField] private float doorOpenAngle = 78f;
        [SerializeField] private float doorAnimationSpeed = 2.5f;

        [Header("Component Highlights")]
        [SerializeField] private Material highlightMaterial;
        [SerializeField] private Material ghostMaterial;

        [Header("Explode View Settings")]
        [SerializeField] private float maxExplodeDistance = 0.45f;

        private bool isDoorOpen = false;
        private Coroutine doorCoroutine;
        private string selectedComponentId = null;

        // Caches for materials and transforms
        private Dictionary<Renderer, Material[]> originalMaterials = new Dictionary<Renderer, Material[]>();
        private Dictionary<Transform, Vector3> initialLocalPositions = new Dictionary<Transform, Vector3>();
        private Dictionary<string, List<Renderer>> componentRenderers = new Dictionary<string, List<Renderer>>();

        public event Action<bool> OnDoorStateChanged;
        public event Action<string> OnComponentSelected;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;

            AutoDiscoverHierarchy();
        }

        private void AutoDiscoverHierarchy()
        {
            if (leftDoorHinge == null)
            {
                var t = transform.Find("10_Fresh_Food_Door_Assembly");
                if (t != null) leftDoorHinge = t;
            }
            if (rightDoorHinge == null)
            {
                var t = transform.Find("11_Freezer_Door_Assembly");
                if (t != null) rightDoorHinge = t;
            }

            // Cache renderers and original materials
            var allRenderers = GetComponentsInChildren<Renderer>(true);
            foreach (var r in allRenderers)
            {
                originalMaterials[r] = r.sharedMaterials;
                initialLocalPositions[r.transform] = r.transform.localPosition;

                // Find top group parent under root
                Transform p = r.transform;
                string compId = "";
                while (p != null && p.parent != transform && p.parent != null)
                {
                    p = p.parent;
                }
                if (p != null && p.parent == transform)
                {
                    compId = p.name;
                    if (!componentRenderers.ContainsKey(compId))
                        componentRenderers[compId] = new List<Renderer>();
                    componentRenderers[compId].Add(r);
                }
            }
        }

        #region Door Controls

        public bool IsDoorOpen => isDoorOpen;

        public void ToggleDoors()
        {
            SetDoorsOpen(!isDoorOpen);
        }

        public void SetDoorsOpen(bool open)
        {
            if (isDoorOpen == open && doorCoroutine == null) return;
            isDoorOpen = open;
            if (doorCoroutine != null) StopCoroutine(doorCoroutine);
            doorCoroutine = StartCoroutine(AnimateDoorsRoutine(open));
            OnDoorStateChanged?.Invoke(isDoorOpen);
        }

        private IEnumerator AnimateDoorsRoutine(bool open)
        {
            float targetAngleL = open ? doorOpenAngle : 0f;
            float targetAngleR = open ? -doorOpenAngle : 0f;

            Quaternion startRotL = leftDoorHinge ? leftDoorHinge.localRotation : Quaternion.identity;
            Quaternion endRotL = Quaternion.Euler(0f, targetAngleL, 0f);

            Quaternion startRotR = rightDoorHinge ? rightDoorHinge.localRotation : Quaternion.identity;
            Quaternion endRotR = Quaternion.Euler(0f, targetAngleR, 0f);

            float t = 0f;
            while (t < 1f)
            {
                t += Time.deltaTime * doorAnimationSpeed;
                float ease = Mathf.SmoothStep(0f, 1f, t);

                if (leftDoorHinge) leftDoorHinge.localRotation = Quaternion.Slerp(startRotL, endRotL, ease);
                if (rightDoorHinge) rightDoorHinge.localRotation = Quaternion.Slerp(startRotR, endRotR, ease);
                yield return null;
            }

            if (leftDoorHinge) leftDoorHinge.localRotation = endRotL;
            if (rightDoorHinge) rightDoorHinge.localRotation = endRotR;
            doorCoroutine = null;
        }

        #endregion

        #region Component Selection & Highlight

        public string SelectedComponentId => selectedComponentId;

        public void SelectComponent(string componentId)
        {
            selectedComponentId = componentId;
            RestoreAllMaterials();

            if (!string.IsNullOrEmpty(componentId))
            {
                HighlightComponent(componentId);
            }
            OnComponentSelected?.Invoke(selectedComponentId);
        }

        public void ClearSelection()
        {
            SelectComponent(null);
        }

        private void HighlightComponent(string compId)
        {
            if (!componentRenderers.TryGetValue(compId, out var renderers)) return;

            foreach (var r in renderers)
            {
                if (highlightMaterial != null)
                {
                    Material[] highlighted = new Material[r.sharedMaterials.Length];
                    for (int i = 0; i < highlighted.Length; i++) highlighted[i] = highlightMaterial;
                    r.materials = highlighted;
                }
            }
        }

        public void SetIsolateMode(bool isolate)
        {
            if (string.IsNullOrEmpty(selectedComponentId)) return;

            foreach (var kvp in componentRenderers)
            {
                bool isSelected = kvp.Key == selectedComponentId;
                foreach (var r in kvp.Value)
                {
                    if (isolate)
                    {
                        if (!isSelected)
                        {
                            if (ghostMaterial != null)
                            {
                                Material[] ghosted = new Material[r.sharedMaterials.Length];
                                for (int i = 0; i < ghosted.Length; i++) ghosted[i] = ghostMaterial;
                                r.materials = ghosted;
                            }
                            else
                            {
                                r.enabled = false;
                            }
                        }
                    }
                    else
                    {
                        r.enabled = true;
                    }
                }
            }

            if (!isolate)
            {
                RestoreAllMaterials();
                if (!string.IsNullOrEmpty(selectedComponentId))
                {
                    HighlightComponent(selectedComponentId);
                }
            }
        }

        public void RestoreAllMaterials()
        {
            foreach (var kvp in originalMaterials)
            {
                if (kvp.Key != null)
                {
                    kvp.Key.enabled = true;
                    kvp.Key.sharedMaterials = kvp.Value;
                }
            }
        }

        #endregion

        #region Exploded View

        public void SetExplodeFactor(float factor)
        {
            factor = Mathf.Clamp01(factor);
            foreach (var kvp in componentRenderers)
            {
                string id = kvp.Key;
                Vector3 explodeOffset = GetExplodeOffset(id) * (factor * maxExplodeDistance);
                Transform parentT = transform.Find(id);
                if (parentT != null)
                {
                    parentT.localPosition = explodeOffset;
                }
            }
        }

        private Vector3 GetExplodeOffset(string id)
        {
            switch (id)
            {
                case "01_Compressor": return new Vector3(-0.5f, 0f, -0.6f);
                case "02_Condenser_Coil": return new Vector3(0f, 0f, -0.9f);
                case "03_Capillary_Tube": return new Vector3(0.3f, 0.2f, -0.5f);
                case "04_Evaporator_Unit": return new Vector3(0f, 0.4f, 0.5f);
                case "05_Filter_Drier": return new Vector3(0.5f, -0.2f, -0.4f);
                case "06_Condenser_Fan": return new Vector3(0.6f, 0f, -0.7f);
                case "07_Refrigerant_Lines": return new Vector3(-0.3f, 0f, -0.4f);
                case "09_Shelves_And_Drawers": return new Vector3(0f, 0.8f, 0.3f);
                case "10_Fresh_Food_Door_Assembly": return new Vector3(-0.7f, 0.3f, 0.6f);
                case "11_Freezer_Door_Assembly": return new Vector3(0.7f, 0.3f, 0.6f);
                case "12_Rear_Ventilation_Grille": return new Vector3(0f, 0f, -1.2f);
                case "13_Thermostat_Electrical": return new Vector3(-0.6f, 0.4f, 0.2f);
                default: return Vector3.zero;
            }
        }

        #endregion
    }
}
