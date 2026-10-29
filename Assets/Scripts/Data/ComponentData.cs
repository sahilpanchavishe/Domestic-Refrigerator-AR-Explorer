using System;
using System.Collections.Generic;
using UnityEngine;

namespace DomesticRefrigerator.Data
{
    [System.Serializable]
    public class ComponentData
    {
        public string id;
        public int number;
        public string name;
        public string shortDescription;
        public string detailedDescription;
        public string function;
        public string workingPrinciple;
        public string location;
        public string cycleRole;
        public string practicalRelevance;
        public string studentNote;
    }

    [System.Serializable]
    public class ComponentDatabaseWrapper
    {
        public List<ComponentData> components;
    }
}
