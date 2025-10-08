// DictionaryRepository.js
class DictionaryRepository {
    constructor() {
        this.api = "https://lexicc.caroycuervo.gov.co/api/";
    }
    
    getHeaders = () => {
        return {
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${sessionStorage.getItem("accessToken")}`
        };
    }
    async fetchAttributes(dictionaryId) {
        const dictionaryAttributeUrl = dictionaryId
            ? `${this.api}lexicc/v1/dictionary-attribute/?idDictionary=${dictionaryId}`
            : false;
        try {
            const attributes = await fetch(dictionaryAttributeUrl).then(res => res.json());
            return attributes.data;
        } catch (error) {
            console.error("Error fetching attributes:", error);
            throw error;
        }
    }

    async updateItem(url, data) {
        if (source === 'localStorage') {
            // Implement localStorage update logic if needed
        } else if (source === 'api') {
            await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
        }
    }

    async deleteItem(url) {
        if (source === 'localStorage') {
            // Implement localStorage delete logic if needed
        } else if (source === 'api') {
            await fetch(url, {
                method: 'DELETE',
            });
        }
    }




    async fetchAttributes(dictionaryId, source) {
        if (source === 'localStorage') {
            const attributes = localStorage.getItem("dictionary-attribute");
            return Promise.resolve(attributes ? JSON.parse(attributes) : []);
        } else {
            if (!dictionaryId) {
                return [];
            }
            const response = await fetch(`${this.api}lexicc/v1/dictionary-attribute/?idDictionary=${dictionaryId}`);
            const data = await response.json();
            return Promise.resolve(data.data)
        }
    };

    async fetchDictionary(dictionaryId, source) {
        if (source === 'localStorage') {
            const dictionary = localStorage.getItem("dictionaryInfo");
            return Promise.resolve(dictionary ? JSON.parse(dictionary) : {});
        } else {
            if (!dictionaryId) {
                return {};
            }
            const response = await fetch(`${this.api}lexicc/v1/dictionaryInfo/${dictionaryId}`);
            const data = await response.json();
            return Promise.resolve(data.data)
        }
    }

    async fetchDictionaryStructure(dictionaryId, source) {
        if (source === 'localStorage') {
            const structure = localStorage.getItem("dictionary-structure");
            return Promise.resolve(structure ? JSON.parse(structure) : []);

        } else {
            if (!dictionaryId) {
                return [];
            }
            const response = await fetch(`${this.api}lexicc/v1/dictionary-structure/?idDictionary=${dictionaryId}`);
            const data = await response.json();
            return Promise.resolve(data.data)
        }
    }

    async addDictionaryStructureElement(structureElement, source) {
        try {
            if (source === 'localStorage') {
                const currentLocalStorageStructure = localStorage.getItem("dictionary-structure") ? JSON.parse(localStorage.getItem("dictionary-structure")) : [];
                const newId = `ls_${Date.now()}`;
                localStorage.setItem("dictionary-structure", JSON.stringify([...currentLocalStorageStructure, {
                    ...structureElement,
                    _id: newId
                }]));

            } else if (source === 'api') {
                const url = `${this.api}lexicc/v1/dictionary-structure`;
                const response = await fetch(url, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json; charset=utf-8",
                    },
                    body: JSON.stringify(structureElement),
                });
                return response.json();
            }
        } catch (error) {
            console.error("Error creating dictionary structure element:", error);
            throw error;
        }
    }

    async editDictionaryStructureElement(structureElement, source) {
        try {
            if (source === 'localStorage') {
                const currentLocalStorageStructure = localStorage.getItem("dictionary-structure") ? JSON.parse(localStorage.getItem("dictionary-structure")) : [];
                const newStructure = currentLocalStorageStructure.map(item => {
                    if (item._id === structureElement._id) {
                        return structureElement;
                    }
                    return item;
                });
                localStorage.setItem("dictionary-structure", JSON.stringify(newStructure));

            } else if (source === 'api') {
                const url = `${this.api}lexicc/v1/dictionary-structure/${structureElement._id}`;
                await fetch(url, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(structureElement),
                });
            }
        } catch (error) {
            console.error("Error editing dictionary structure element:", error);
            throw error;
        }

    }
    async removeDictionaryStructureElement(structureElementId, source) {
        try {
            if (source === 'localStorage') {
                const currentLocalStorageStructure = localStorage.getItem("dictionary-structure") ? JSON.parse(localStorage.getItem("dictionary-structure")) : [];
                const newStructure = currentLocalStorageStructure.filter(item => item._id !== structureElementId);
                localStorage.setItem("dictionary-structure", JSON.stringify(newStructure));
            } else if (source === 'api') {
                const url = `${this.api}lexicc/v1/dictionary-structure/${structureElementId}`;
                await fetch(url, {
                    method: 'DELETE',
                });
            }
            this.removeAttributeByStructureElementId(structureElementId, source);
        } catch (error) {
            console.error("Error deleting dictionary structure element:", error);
            throw error;
        }
    }

    async moveItem(structureItem, source) {
        if (source === 'localStorage') {
            const currentLocalStorageStructure = localStorage.getItem("dictionary-structure") ? JSON.parse(localStorage.getItem("dictionary-structure")) : [];
            const newStructure = currentLocalStorageStructure.map(item => {
                if (item._id === structureItem._id) {
                    return structureItem;
                }
                return item;
            });
            localStorage.setItem("dictionary-structure", JSON.stringify(newStructure));

        } else if (source === 'api') {
            const url = `${this.api}lexicc/v1/dictionary-structure/${structureItem._id}`;
            await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(structureItem),
            });

        }
    }




    async addAttribute(attribute, source) {
        try {
            if (source === 'localStorage') {
                const newId = `ls_${Date.now()}`;
                const currentAttributes = localStorage.getItem("dictionary-attribute") ? JSON.parse(localStorage.getItem("dictionary-attribute")) : [];
                localStorage.setItem("dictionary-attribute", JSON.stringify([...currentAttributes, { ...attribute, _id: newId }]));
            } else {
                const url = `${this.api}lexicc/v1/dictionary-attribute`;
                const response = await fetch(url, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(attribute),
                });
                return response.json();
            }

        } catch (error) {
            console.error("Error creating dictionary attribute:", error);
            throw error;
        }
    }

    async removeAttribute(attributeId, source) {
        try {
            if (source === 'localStorage') {
                const currentAttributes = localStorage.getItem("dictionary-attribute") ? JSON.parse(localStorage.getItem("dictionary-attribute")) : [];
                const newAttributes = currentAttributes.filter(item => item._id !== attributeId);
                localStorage.setItem("dictionary-attribute", JSON.stringify(newAttributes));
            } else {
                const url = `${this.api}lexicc/v1/dictionary-attribute/${attributeId}`;
                await fetch(url, {
                    method: 'DELETE',
                });
            }
        } catch (error) {
            console.error("Error deleting dictionary attribute:", error);
            throw error;
        }
    }

    async removeAttributeByStructureElementId(structureElementId, source) {
        try {
            if (source === 'localStorage') {
                const currentAttributes = localStorage.getItem("dictionary-attribute") ? JSON.parse(localStorage.getItem("dictionary-attribute")) : [];
                const newAttributes = currentAttributes.filter(item => item.idLabel !== structureElementId);
                localStorage.setItem("dictionary-attribute", JSON.stringify(newAttributes));
            } else {
                const url = `${this.api}lexicc/v1/dictionary-attribute/${attributeId}`;
                await fetch(url, {
                    method: 'DELETE',
                });
            }
        } catch (error) {
            console.error("Error deleting dictionary attribute:", error);
            throw error;
        }
    }




    async loadData(dictionaryId, selectedLetter, source) {
        try {
            const [form, entries, dictionary, attributes] = await Promise.all(
                [
                    this.fetchDictionaryStructure(dictionaryId, source),
                    this.fetchDictionaryEntries(dictionaryId, selectedLetter, source),
                    this.fetchDictionary(dictionaryId, source),
                    this.fetchAttributes(dictionaryId, source)
                ]
            );
            return {
                form: form,
                entries: entries,
                dictionary: dictionary,
                attributes: attributes
            }
        } catch (error) {
            console.error("Error loading data:", error);
            throw error;
        }
    }

    async updateDictionary(dictionaryId, dictionaryData) {
        const url = `${this.api}lexicc/v1/dictionary/${dictionaryId}`;
        try {
            const response = await fetch(url, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(dictionaryData),
            });
            return response.json();
        } catch (error) {
            console.error("Error updating dictionary:", error);
            throw error;
        }
    }

    async createDictionary(dictionaryData) {
        const url = `${this.api}lexicc/v1/dictionary`;
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: this.getHeaders(),
                body: JSON.stringify(dictionaryData),
            });
            return response.json();
        } catch (error) {
            console.error("Error creating dictionary:", error);
            throw error;
        }
    }

    async assignDictionaryToUser(data) {
        const url = `${this.api}lexicc/v1/updateUser/${data._id}`;
        try {
            const response = await fetch(url, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ dictionaries: data.dictionaries }),
            });
            return response.json();
        } catch (error) {
            console.error("Error assigning dictionary to user:", error);
            throw error;
        }
    }
    async fetchDictionaryEntries(dictionaryId, selectedLetter, source) {
        if (source === 'localStorage') {
            const entries = localStorage.getItem("dictionary-entries");
            return Promise.resolve(entries ? JSON.parse(entries) : []);
        } else {
            if (!dictionaryId) {
                return [];
            }
            const response = await fetch(`${this.api}lexicc/v1/dictionary-data/?tagName=lemmaSign&name=^${selectedLetter}&idDictionary=${dictionaryId}`);
            const data = await response.json();
            return Promise.resolve(data.data)
        }
    }

    async createDictionaryEntry(entry, source) {
        if (source === 'localStorage') {
            const currentLocalStorageEntries = localStorage.getItem("dictionary-entries") ? JSON.parse(localStorage.getItem("dictionary-entries")) : [];
            const newId = `ls_${Date.now()}`;
            localStorage.setItem("dictionary-entries", JSON.stringify([...currentLocalStorageEntries, { ...entry, _id: newId }]));
        } else if (source === 'api') {
            const url = `${this.api}lexicc/v1/dictionary-data`;
            await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(entry),
            });
        }
    }

    async updateDictionaryEntry(entry, source) {

        if (source === 'localStorage') {
            const currentLocalStorageEntries = localStorage.getItem("dictionary-entries") ? JSON.parse(localStorage.getItem("dictionary-entries")) : [];
            const newEntries = currentLocalStorageEntries.map(item => {
                if (item._id === entry._id) {
                    return entry;
                }
                return item;
            });
            localStorage.setItem("dictionary-entries", JSON.stringify(newEntries));
        } else if (source === 'api') {
            const url = `${this.api}lexicc/v1/dictionary-data/${entry._id}`;
            await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(entry),
            });
        }
    }

    async deleteEntry(entryId, source) {
        if (source === 'localStorage') {
            const currentLocalStorageEntries = localStorage.getItem("dictionary-entries") ? JSON.parse(localStorage.getItem("dictionary-entries")) : [];
            const newEntries = currentLocalStorageEntries.filter(item => item._id !== entryId);
            localStorage.setItem("dictionary-entries", JSON.stringify(newEntries));
        } else if (source === 'api') {
            const url = `${this.api}lexicc/v1/dictionary-data/${entryId}`;
            await fetch(url, {
                method: 'DELETE',
            });
        }
    }

    // Add other CRUD operations as needed
}

export default DictionaryRepository;