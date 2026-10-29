using System;
using System.Collections.Generic;
using UnityEngine;

namespace DomesticRefrigerator.Data
{
    public class ComponentDatabase : MonoBehaviour
    {
        public static ComponentDatabase Instance { get; private set; }

        [SerializeField] private TextAsset jsonFile;
        private List<ComponentData> components = new List<ComponentData>();
        private Dictionary<string, ComponentData> componentMap = new Dictionary<string, ComponentData>();

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;
            LoadDatabase();
        }

        public void LoadDatabase()
        {
            string jsonText = "";
            if (jsonFile != null)
            {
                jsonText = jsonFile.text;
            }
            else
            {
                TextAsset loadedAsset = Resources.Load<TextAsset>("Data/refrigerator_components");
                if (loadedAsset != null) jsonText = loadedAsset.text;
            }

            if (!string.IsNullOrEmpty(jsonText))
            {
                try
                {
                    // If JSON is array, wrap it
                    string wrapped = jsonText.TrimStart().StartsWith("[") 
                        ? "{\"components\":" + jsonText + "}" 
                        : jsonText;
                    ComponentDatabaseWrapper wrapper = JsonUtility.FromJson<ComponentDatabaseWrapper>(wrapped);
                    components = wrapper.components;
                    componentMap.Clear();
                    foreach (var c in components)
                    {
                        componentMap[c.id] = c;
                    }
                    Debug.Log($"Loaded {components.Count} refrigeration components successfully.");
                }
                catch (Exception e)
                {
                    Debug.LogError("Failed to parse refrigerator components JSON: " + e.Message);
                }
            }
        }

        public List<ComponentData> GetAllComponents() => components;

        public ComponentData GetComponentById(string id)
        {
            if (string.IsNullOrEmpty(id)) return null;
            componentMap.TryGetValue(id, out var data);
            return data;
        }

        public ComponentData GetComponentByNumber(int number)
        {
            return components.Find(c => c.number == number);
        }
    }
}
