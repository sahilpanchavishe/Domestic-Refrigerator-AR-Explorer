using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using DomesticRefrigerator.Core;
using DomesticRefrigerator.Data;

namespace DomesticRefrigerator.UI
{
    public class UIController : MonoBehaviour
    {
        [Header("Information Panel")]
        [SerializeField] private GameObject infoPanel;
        [SerializeField] private Text componentNumberText;
        [SerializeField] private Text componentNameText;
        [SerializeField] private Text shortDescriptionText;
        [SerializeField] private Text functionText;
        [SerializeField] private Text principleText;
        [SerializeField] private Text locationText;
        [SerializeField] private Text cycleRoleText;
        [SerializeField] private Text practicalText;
        [SerializeField] private Text studentNoteText;

        [Header("Control Buttons")]
        [SerializeField] private Button doorToggleButton;
        [SerializeField] private Text doorButtonText;
        [SerializeField] private Slider explodeSlider;
        [SerializeField] private Toggle isolateToggle;

        [Header("Camera & View Preset Buttons")]
        [SerializeField] private OrbitCameraController orbitCamera;
        [SerializeField] private Button frontViewButton;
        [SerializeField] private Button rearViewButton;
        [SerializeField] private Button interiorViewButton;
        [SerializeField] private Button resetViewButton;

        [Header("Navigation Buttons")]
        [SerializeField] private Button prevComponentButton;
        [SerializeField] private Button nextComponentButton;
        [SerializeField] private Button closeInfoButton;

        [Header("Credits & About")]
        [SerializeField] private GameObject aboutModal;
        [SerializeField] private Text creditsText;

        private int currentComponentIndex = -1;
        private List<ComponentData> allComponents = new List<ComponentData>();

        private void Start()
        {
            if (ComponentDatabase.Instance != null)
            {
                allComponents = ComponentDatabase.Instance.GetAllComponents();
            }

            if (RefrigeratorController.Instance != null)
            {
                RefrigeratorController.Instance.OnDoorStateChanged += HandleDoorStateChanged;
                RefrigeratorController.Instance.OnComponentSelected += HandleComponentSelected;
            }

            // Hook UI listeners
            if (doorToggleButton) doorToggleButton.onClick.AddListener(OnDoorToggleClicked);
            if (explodeSlider) explodeSlider.onValueChanged.AddListener(OnExplodeSliderChanged);
            if (isolateToggle) isolateToggle.onValueChanged.AddListener(OnIsolateToggleChanged);

            if (frontViewButton) frontViewButton.onClick.AddListener(() => SetCameraPreset("front"));
            if (rearViewButton) rearViewButton.onClick.AddListener(() => SetCameraPreset("rear"));
            if (interiorViewButton) interiorViewButton.onClick.AddListener(() => SetCameraPreset("interior"));
            if (resetViewButton) resetViewButton.onClick.AddListener(() => SetCameraPreset("reset"));

            if (prevComponentButton) prevComponentButton.onClick.AddListener(OnPrevComponent);
            if (nextComponentButton) nextComponentButton.onClick.AddListener(OnNextComponent);
            if (closeInfoButton) closeInfoButton.onClick.AddListener(OnCloseInfoClicked);

            UpdateDoorButton(false);
            if (infoPanel) infoPanel.SetActive(false);

            if (creditsText != null)
            {
                creditsText.text = "Domestic Refrigerator AR Explorer\n" +
                                   "COEP Technological University, Pune — Robotics and AI\n" +
                                   "Prepared by:\n" +
                                   "• Sahil Panchavishe — 612302040\n" +
                                   "• Megh Shidam — 612302058";
            }
        }

        private void OnDestroy()
        {
            if (RefrigeratorController.Instance != null)
            {
                RefrigeratorController.Instance.OnDoorStateChanged -= HandleDoorStateChanged;
                RefrigeratorController.Instance.OnComponentSelected -= HandleComponentSelected;
            }
        }

        private void OnDoorToggleClicked()
        {
            if (RefrigeratorController.Instance != null)
                RefrigeratorController.Instance.ToggleDoors();
        }

        private void HandleDoorStateChanged(bool isOpen)
        {
            UpdateDoorButton(isOpen);
        }

        private void UpdateDoorButton(bool isOpen)
        {
            if (doorButtonText != null)
            {
                doorButtonText.text = isOpen ? "Close Doors" : "Open Doors";
            }
        }

        private void OnExplodeSliderChanged(float val)
        {
            if (RefrigeratorController.Instance != null)
                RefrigeratorController.Instance.SetExplodeFactor(val);
        }

        private void OnIsolateToggleChanged(bool isolate)
        {
            if (RefrigeratorController.Instance != null)
                RefrigeratorController.Instance.SetIsolateMode(isolate);
        }

        private void SetCameraPreset(string preset)
        {
            if (orbitCamera != null) orbitCamera.SetViewPreset(preset);
            if (preset == "interior" && RefrigeratorController.Instance != null)
            {
                RefrigeratorController.Instance.SetDoorsOpen(true);
            }
        }

        private void HandleComponentSelected(string compId)
        {
            if (string.IsNullOrEmpty(compId))
            {
                if (infoPanel) infoPanel.SetActive(false);
                currentComponentIndex = -1;
                return;
            }

            var comp = ComponentDatabase.Instance != null ? ComponentDatabase.Instance.GetComponentById(compId) : null;
            if (comp != null)
            {
                currentComponentIndex = allComponents.FindIndex(c => c.id == compId);
                DisplayComponentData(comp);
            }
        }

        private void DisplayComponentData(ComponentData comp)
        {
            if (infoPanel) infoPanel.SetActive(true);

            if (componentNumberText) componentNumberText.text = $"PART #{comp.number:00}";
            if (componentNameText) componentNameText.text = comp.name;
            if (shortDescriptionText) shortDescriptionText.text = comp.shortDescription;
            if (functionText) functionText.text = comp.function;
            if (principleText) principleText.text = comp.workingPrinciple;
            if (locationText) locationText.text = comp.location;
            if (cycleRoleText) cycleRoleText.text = comp.cycleRole;
            if (practicalText) practicalText.text = comp.practicalRelevance;
            if (studentNoteText) studentNoteText.text = comp.studentNote;
        }

        private void OnPrevComponent()
        {
            if (allComponents.Count == 0) return;
            currentComponentIndex--;
            if (currentComponentIndex < 0) currentComponentIndex = allComponents.Count - 1;
            SelectByIndex(currentComponentIndex);
        }

        private void OnNextComponent()
        {
            if (allComponents.Count == 0) return;
            currentComponentIndex++;
            if (currentComponentIndex >= allComponents.Count) currentComponentIndex = 0;
            SelectByIndex(currentComponentIndex);
        }

        private void SelectByIndex(int idx)
        {
            if (idx >= 0 && idx < allComponents.Count)
            {
                string id = allComponents[idx].id;
                if (RefrigeratorController.Instance != null)
                    RefrigeratorController.Instance.SelectComponent(id);
            }
        }

        private void OnCloseInfoClicked()
        {
            if (RefrigeratorController.Instance != null)
                RefrigeratorController.Instance.ClearSelection();
        }

        public void ToggleAboutModal(bool show)
        {
            if (aboutModal) aboutModal.SetActive(show);
        }
    }
}
