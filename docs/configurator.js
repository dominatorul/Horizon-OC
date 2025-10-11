/* configurator.js
   Clean, readable reconstruction of the original minified configurator
   - Keeps original behavior (tables, parsing, localStorage, GitHub release fetching)
   - Uses modern async/await and DOMContentLoaded guarding
*/

const CUST_REV_ADV = 11;

const CustPlatform = Object.freeze({
  Undefined: 0,
  Erista: 1,
  Mariko: 2,
  All: 3
});

class CustEntry {
  constructor(id, name, platform, size, desc = [], defval = 0, range = [0, 1e6], step = 1, zeroable = true) {
    this.id = id;
    this.name = name;
    this.platform = platform;
    this.size = size;
    this.desc = desc;
    this.defval = defval;
    this.step = step;
    this.zeroable = zeroable;
    this.min = range[0];
    this.max = range[1];
    this.value = this.defval;
  }

  validate() {
    const err = new ErrorToolTip(this.id).clear();
    if (Number.isNaN(this.value) || this.value === undefined) {
      err.setMsg("Invalid value: Not a number").show();
      return false;
    }
    if (!this.zeroable && this.value === 0) {
      err.setMsg("Zero is not allowed for this entry").show();
      return false;
    }
    if (this.value < this.min || this.value > this.max) {
      err.setMsg(`Expected range: [${this.min}, ${this.max}], got ${this.value}.`).show();
      return false;
    }
    if ((this.value % this.step) !== 0) {
      err.setMsg(`${this.value} % ${this.step} ≠ 0`).show();
      return false;
    }
    return true;
  }

  getInputElement() {
    return document.getElementById(this.id);
  }

  updateValueFromElement() {
    const el = this.getInputElement();
    this.value = Number(el?.value);
  }

  isAvailableFor(platform) {
    return platform === CustPlatform.Undefined || this.platform === platform || this.platform === CustPlatform.All;
  }

  createElement(containerId = "config-list-basic") {
    let input = this.getInputElement();
    if (!input) {
      const wrapper = document.createElement("div");
      wrapper.classList.add("grid", "cust-element", "mb-3");

      input = document.createElement("input");
      input.min = String(this.zeroable ? 0 : this.min);
      input.max = String(this.max);
      input.id = this.id;
      input.type = "number";
      input.step = String(this.step);
      input.classList.add("text-black", "w-36");

      const label = document.createElement("label");
      label.setAttribute("for", this.id);
      label.innerHTML = `<strong>${this.name}</strong>`;
      label.classList.add("block", "mb-1");

      const desc = document.createElement("blockquote");
      desc.innerHTML = "<ul>" + (this.desc || []).map(d => `<li>${d}</li>`).join("") + "</ul>";
      desc.setAttribute("for", this.id);
      desc.classList.add("text-sm", "text-gray-300");

      wrapper.appendChild(label);
      wrapper.appendChild(input);
      wrapper.appendChild(desc);

      const container = document.getElementById(containerId);
      if (container) container.appendChild(wrapper);
      new ErrorToolTip(this.id).addChangeListener();
    }
    input.value = String(this.value);
  }

  setElementValue() {
    const el = this.getInputElement();
    if (el) el.value = String(this.value);
  }

  setElementDefaultValue() {
    const el = this.getInputElement();
    if (el) el.value = String(this.defval);
  }

  removeElement() {
    const el = this.getInputElement();
    if (el && el.parentElement && el.parentElement.parentElement) el.parentElement.parentElement.remove();
  }

  showElement() {
    const el = this.getInputElement();
    if (el && el.parentElement && el.parentElement.parentElement) el.parentElement.parentElement.style.removeProperty("display");
  }

  hideElement() {
    const el = this.getInputElement();
    if (el && el.parentElement && el.parentElement.parentElement) el.parentElement.parentElement.style.setProperty("display", "none");
  }
}

class AdvEntry extends CustEntry {
  createElement() {
    super.createElement("config-list-advanced");
  }
}

class GpuEntry extends CustEntry {
  constructor(id, name, platform = CustPlatform.Mariko, size = 4, desc = ["range: 610 ≤ x ≤ 1000"], defval = 610, range = [610, 1000], step = 5, zeroable = false) {
    super(id, name, platform, size, desc, defval, range, step, zeroable);
  }

  createElement() {
    super.createElement("config-list-gpu");
  }
}

/* === Tables (reconstructed from original) ===
   Note: Numeric defaults preserved where feasible.
*/
const CustTable = [
  new CustEntry("mtcConf", "DRAM Timing", CustPlatform.All, 4,
    [
      "<b>0</b>: AUTO_ADJ: Auto adjust mtc table with LPDDR4 4266 Mbps specs, 16Gb density."
    ], 0, [0, 2], 0),
  new CustEntry("commonCpuBoostClock", "Boost Clock in kHz", CustPlatform.All, 4,
    ["System default: 1785000", "Boost clock will be applied when applications request Boost Mode via performance configuration."],
    1785000, [1020000, 3000000], 1, false),
  new CustEntry("commonEmcMemVolt", "EMC Vdd2 Voltage in uV", CustPlatform.All, 4,
    ["Acceptable range: 1100000 ≤ x ≤ 1237500, and it should be divided evenly by 12500.", "Erista Default: 1125000", "Mariko Default: 1100000", "Official lpddr4(x) range: 1060mV~1175mV (1100mV nominal)", "OCS need high voltage unlike l4t because of not scaling mtc table well. However it is recommended to stay within official limits", "Not enabled by default"],
    1175000, [1100000, 1237500], 12500),
  new CustEntry("eristaCpuMaxVolt", "Erista CPU Max Voltage in mV", CustPlatform.Erista, 4,
    ["Acceptable range: 1120 ≤ x ≤ 1300", "L4T Default: 1235"], 1235, [1120, 1300], 1),
  new CustEntry("eristaEmcMaxClock", "Erista RAM Max Clock in kHz", CustPlatform.Erista, 4,
    ["Values should be ≥ 1600000, and divided evenly by 3200.", "Recommended Clocks: 1862400, 2131200 (JEDEC)", "<b>WARNING:</b> RAM overclock could be UNSTABLE if timing parameters are not suitable for your DRAM"], 1600000, [1600000, 2131200], 3200),
  new CustEntry("marikoCpuMaxVolt", "Mariko CPU Max Voltage in mV", CustPlatform.Mariko, 4,
    ["System default: 1120", "Acceptable range: 1120 ≤ x ≤ 1300", "Changing this value affects cpu voltage calculation"], 1235, [1120, 1300], 5),
  new CustEntry("marikoEmcMaxClock", "Mariko RAM Max Clock in kHz", CustPlatform.Mariko, 4,
    ["Values should be ≥ 1600000, and divided evenly by 3200.", "Recommended Clocks: 1862400, 2131200, 2400000 (JEDEC)", "Some clocks above 2400Mhz might not boot, because OCS doesn't scale table very well", "<b>WARNING:</b> RAM overclock could be UNSTABLE if timing parameters are not suitable for your DRAM."],
    18624, [1600000, 2502400], 3200),
  new CustEntry("marikoEmcVddqVolt", "EMC Vddq (Mariko Only) Voltage in uV", CustPlatform.Mariko, 4,
    ["Acceptable range: 550000 ≤ x ≤ 650000", "Value should be divided evenly by 5000", "Default: 600000", "Official lpddr4(x) range: 570mV~650mV (600mV nominal)", "Not enabled by default."],
    0, [550000, 650000], 5000),
  new CustEntry("marikoCpuUV", "Mariko CPU Undervolt", CustPlatform.Mariko, 4,
    ["Reduce CPU power draw", "Your CPU might not withstand undervolt, and can hang your console, or crash games", "Undervolting too much will drop CPU performance even if it seems stable", "CPU voltages are dynamic and will change with temperature and gpu speedo"],
    0, [0, 8], 1),
  new CustEntry("marikoGpuUV", "EMariko GPU Undervolt", CustPlatform.Mariko, 4,
    ["Reduce GPU power draw", "Your GPU might not withstand undervolt, and can hang your console, or crash games", "Undervolting too much will drop GPU performance even if it seems stable", "GPU voltages are dynamic and will change with temperature and gpu speedo", "<b>0</b> : Default Table", "<b>1</b> : Undervolt Level 1 (SLT: Aggressive)", "<b>2</b> : Undervolt Level 2 (HiOPT: Drastic)", "<b>3</b> : Custom static GPU Voltage Table (Use Gpu Configuration below)"],
    0, [0, 3], 1),

    new CustEntry("eristaCpuUv", "Mariko CPU Undervolt", CustPlatform.Erista, 4,
    ["Reduce CPU power draw", "Your CPU might not withstand undervolt, and can hang your console, or crash games", "Undervolting too much will drop CPU performance even if it seems stable", "CPU voltages are dynamic and will change with temperature and gpu speedo"],
    0, [0, 5], 1),
    new CustEntry("eristaGpuUv", "EMariko GPU Undervolt", CustPlatform.Erista, 4,
    ["Reduce GPU power draw", "Your GPU might not withstand undervolt, and can hang your console, or crash games", "Undervolting too much will drop GPU performance even if it seems stable", "GPU voltages are dynamic and will change with temperature and gpu speedo", "<b>0</b> : Default Table", "<b>1</b> : Undervolt Level 1 (SLT: Aggressive)", "<b>2</b> : Undervolt Level 2 (HiOPT: Drastic)", "<b>3</b> : Custom static GPU Voltage Table (Use Gpu Configuration below)"],
    0, [0, 3], 1),

  new CustEntry("commonGpuVoltOffset", "GPU Volt Offset", CustPlatform.All, 4,
    ["Negative Voltage offset value for gpu dynamic voltage calculation", "For example, value of 10 will decrease 10mV gpu volt from all frequencies", "Default gpu vmin: Erista - 812.5mV / Mariko - 610mV", "Acceptable range: 0 ~ 100"],
    0, [0, 25], 1)
];

const AdvTable = [
  new AdvEntry("marikoEmcDvbShift", "Step up Mariko EMC DVB Table", CustPlatform.Mariko, 4,
    ["Each number adds 25mV to SoC voltage", "Helps with stability at higher memory clock", "Acceptable range : 0~9"], 0, [0, 9], 1),
  new AdvEntry("ramTimingPresetOne", "Primary RAM Timing Preset", CustPlatform.Mariko, 4,
    ["<b>WARNING</b>: Unstable timings can corrupt your nand", "Select Timing Preset for both AUTO_ADJ and CUSTOM_ADJ", "Values are : tRCD - tRP - tRAS (tRC = tRP + tRAS)", "<b>0</b> : Do Not Adjust (2400Mhz: 12 - 12 - 28) (CUST_ADJ only)", "<b>1</b> : 18 - 18 - 42 (Default timing)", "<b>2</b> : 17 - 17 - 39", "<b>3</b> : 16 - 16 - 36", "<b>4</b> : 15 - 15 - 34", "<b>5</b> : 14 - 14 - 32", "<b>6</b> : 13 - 13 - 30"],
    1, [0, 6], 1),
  new AdvEntry("ramTimingPresetTwo", "Secondary RAM Timing Preset", CustPlatform.Mariko, 4,
    ["WARNING: Unstable timings can corrupt your nand", "Secondary Timing Preset for both AUTO_ADJ and CUSTOM_ADJ", "Values are : tRRD - tFAW", "<b>0</b> : Do Not Adjust (2400Mhz: 6.6 - 26.6) (CUST_ADJ only)", "<b>1</b> : 10 - 40 (Default timing) (3733 specs)", "<b>2</b> : 7.5 - 30 (4266 specs)", "<b>3</b> : 6 - 24", "<b>4</b> : 4 - 16", "<b>5</b> : 3 - 12"],
    1, [0, 5], 1),
  new AdvEntry("ramTimingPresetThree", "Secondary RAM Timing Preset", CustPlatform.Mariko, 4,
    ["WARNING: Unstable timings can corrupt your nand", "Secondary Timing Preset for both AUTO_ADJ and CUSTOM_ADJ", "Values are : tWR - tRTP", "<b>0</b> : Do Not Adjust (2400Mhz: ?? - 5) (CUST_ADJ only)", "<b>1</b> : 18 - 7.5 (Default timing)", "<b>2</b> : 15 - 7.5", "<b>3</b> : 15 - 6", "<b>4</b> : 12 - 6", "<b>5</b> : 12 - 4", "<b>6</b> : 8 - 4"],
    1, [0, 6], 1),
  new AdvEntry("ramTimingPresetFour", "Secondary RAM Timing Preset", CustPlatform.Mariko, 4,
    ["WARNING: Unstable timings can corrupt your nand", "Secondary Timing Preset for both AUTO_ADJ and CUSTOM_ADJ", "Values are : tRFC", "<b>0</b> : Do Not Adjust (2400Mhz: 93.3) (CUST_ADJ only)", "<b>1</b> : 140 (Default timing)", "<b>2</b> : 120", "<b>3</b> : 100", "<b>4</b> : 80", "<b>5</b> : 70", "<b>6</b> : 60"],
    1, [0, 6], 1),
  new AdvEntry("ramTimingPresetFive", "Secondary RAM Timing Preset", CustPlatform.Mariko, 4,
    ["WARNING: Unstable timings can corrupt your nand", "Secondary Timing Preset for both AUTO_ADJ and CUSTOM_ADJ", "Values are : tWTR", "<b>0</b> : Do Not Adjust (2400Mhz: ??) (CUST_ADJ only)", "<b>1</b> : 10 (Default timing)", "<b>2</b> : 8", "<b>3</b> : 6", "<b>4</b> : 4", "<b>5</b> : 2", "<b>6</b> : 1"],
    1, [0, 6], 1),
  new AdvEntry("ramTimingPresetSix", "Tertiary RAM Timing Preset", CustPlatform.Mariko, 4,
    ["WARNING: Unstable timings can corrupt your nand", "Tertiary Timing Preset for both AUTO_ADJ and CUSTOM_ADJ", "Values are : tREFpb", "<b>0</b> : Do Not Adjust (2400Mhz: 325) (CUST_ADJ only)", "<b>1</b> : 488 (Default timing)", "<b>2</b> : 976", "<b>3</b> : 1952", "<b>4</b> : 3256", "<b>5</b> : MAX"],
    1, [0, 5], 1),
  new AdvEntry("ramTimingPresetSeven", "Latency Decrement", CustPlatform.Mariko, 4,
    ["WARNING: Unstable timings can corrupt your nand", "Latency decrement for both AUTO_ADJ and CUSTOM_ADJ", "This preset decreases Write/Read related delays. Values are Write - Read", "<b>0</b> : 0 - 0, Do Not Adjust for CUST_ADJ", "<b>1</b> : '-2' - '-4'", "<b>2</b> : '-4' - '-8'", "<b>3</b> : '-6' - '-12'", "<b>4</b> : '-8' - '-16'", "<b>5</b> : '-10' - '-20'", "<b>6</b> : '-12' - '-24'"],
    0, [0, 6], 1)
];

const GpuTable = [
  new GpuEntry("0", "76.8"),
  new GpuEntry("1", "153.6"),
  new GpuEntry("2", "230.4"),
  new GpuEntry("3", "307.2"),
  new GpuEntry("4", "384.0"),
  new GpuEntry("5", "460.8"),
  new GpuEntry("6", "537.6"),
  new GpuEntry("7", "614.4"),
  new GpuEntry("8", "691.2"),
  new GpuEntry("9", "768.0"),
  new GpuEntry("10", "844.8"),
  new GpuEntry("11", "921.6"),
  new GpuEntry("12", "998.4"),
  new GpuEntry("13", "1075.2"),
  new GpuEntry("14", "1152.0"),
  new GpuEntry("15", "1228.8"),
  new GpuEntry("16", "1267.2")
];

/* ===== ErrorToolTip ===== */
class ErrorToolTip {
  constructor(id, msg) {
    this.id = id;
    this.msg = msg;
    this.element = document.getElementById(id);
    if (msg) this.setMsg(msg);
  }

  setMsg(msg) {
    this.msg = String(msg);
    return this;
  }

  show() {
    if (this.element) this.element.setAttribute("aria-invalid", "true");
    if (this.msg && this.element) {
      this.element.setAttribute("title", this.msg);
      if (this.element.parentElement) {
        this.element.parentElement.setAttribute("data-tooltip", this.msg);
        this.element.parentElement.setAttribute("data-placement", "top");
      }
    }
    return this;
  }

  clear() {
    if (this.element) this.element.removeAttribute("aria-invalid");
    if (this.element) this.element.removeAttribute("title");
    if (this.element && this.element.parentElement) {
      this.element.parentElement.removeAttribute("data-tooltip");
      this.element.parentElement.removeAttribute("data-placement");
    }
    return this;
  }

  addChangeListener() {
    if (!this.element) return;
    this.element.addEventListener("change", () => {
      const tableEntry = CustTable.find(e => e.id === this.id);
      if (tableEntry) {
        tableEntry.value = Number(this.element.value);
        tableEntry.validate();
      }
    });
  }
}

/* ===== CustStorage ===== */
class CustStorage {
  constructor() {
    this.storage = {};
    this.key = "last_saved";
  }

  updateFromTable() {
    // helper to update and validate each entry
    const updateOne = (entry) => {
      entry.updateValueFromElement();
      if (!entry.validate()) {
        const el = entry.getInputElement();
        if (el) el.focus();
        throw new Error(`Invalid ${entry.name}`);
      }
    };

    CustTable.forEach(updateOne);
    AdvTable.forEach(updateOne);
    GpuTable.forEach(updateOne);

    this.storage = {};
    let t = Object.fromEntries(CustTable.map(e => [e.id, e.value]));
    Object.keys(t).forEach(k => (this.storage[k] = t[k]));
    t = Object.fromEntries(AdvTable.map(e => [e.id, e.value]));
    Object.keys(t).forEach(k => (this.storage[k] = t[k]));
    // GPU table could be included too if desired
  }

  setTable() {
    const keys = Object.keys(this.storage);
    keys.forEach(k => {
      const c = CustTable.find(e => e.id === k);
      if (c) c.value = this.storage[k];
    });
    keys.forEach(k => {
      const a = AdvTable.find(e => e.id === k);
      if (a) a.value = this.storage[k];
    });

    // Set defaults for entries not found
    CustTable.filter(e => !keys.includes(e.id)).forEach(e => e.value = e.defval);
    AdvTable.filter(e => !keys.includes(e.id)).forEach(e => e.value = e.defval);

    // Validate and set element values
    CustTable.forEach(e => {
      if (!e.validate()) {
        const el = e.getInputElement();
        if (el) el.focus();
        throw new Error(`Invalid ${e.name}`);
      }
      e.setElementValue();
    });
    AdvTable.forEach(e => {
      if (!e.validate()) {
        const el = e.getInputElement();
        if (el) el.focus();
        throw new Error(`Invalid ${e.name}`);
      }
      e.setElementValue();
    });
    GpuTable.forEach(e => {
      if (!e.validate()) {
        const el = e.getInputElement();
        if (el) el.focus();
        throw new Error(`Invalid ${e.name}`);
      }
      e.setElementValue();
    });
  }

  save() {
    localStorage.setItem(this.key, JSON.stringify(this.storage));
  }

  load() {
    const raw = localStorage.getItem(this.key);
    if (!raw) return null;
    const parsed = JSON.parse(raw);

    // Filter unknown keys and warn
    const custIds = CustTable.map(e => e.id);
    const ignoredCust = Object.keys(parsed).filter(k => !custIds.includes(k));
    if (ignoredCust.length) console.log("Ignored (cust):", ignoredCust);
    Object.keys(parsed).filter(k => custIds.includes(k)).forEach(k => (this.storage[k] = parsed[k]));

    const advIds = AdvTable.map(e => e.id);
    const ignoredAdv = Object.keys(parsed).filter(k => !advIds.includes(k));
    if (ignoredAdv.length) console.log("Ignored (adv):", ignoredAdv);
    Object.keys(parsed).filter(k => advIds.includes(k)).forEach(k => (this.storage[k] = parsed[k]));

    return this.storage;
  }
}

/* ===== Cust (binary parser/patcher) =====
   This class follows the original structure:
   - find magic in buffer using magicLen, mapper sizes
   - parse data using size-mapped getters/setters
   - produce Blob for download (patched buffer)
*/
class Cust {
  constructor() {
    this.storage = new CustStorage();
    this.magic = 1414747459;     // original magic
    this.magicLen = 4;
    this.mapper = {
      2: { get: (offset) => this.view.getUint16(offset, true), set: (offset, v) => this.view.setUint16(offset, v, true) },
      4: { get: (offset) => this.view.getUint32(offset, true), set: (offset, v) => this.view.setUint32(offset, v, true) }
    };
  }

  findMagicOffset() {
    this.view = new DataView(this.buffer);
    for (let offset = 0; offset < this.view.byteLength; offset += this.magicLen) {
      if (this.mapper[this.magicLen].get(offset) === this.magic) {
        this.beginOffset = offset;
        return;
      }
    }
    throw new Error("Invalid loader.kip file (magic not found)");
  }

  save() {
    // update from table (validate & populate storage)
    this.storage.updateFromTable();

    const writeOne = (entry) => {
      if (!entry.offset && entry.offset !== 0) {
        // If offset is missing in the UI, it's an error in mapping
        const el = entry.getInputElement();
        if (el) el.focus();
        throw new Error(`Failed to get offset for ${entry.name}`);
      }
      const mapper = this.mapper[entry.size];
      if (!mapper) {
        const el = entry.getInputElement();
        if (el) el.focus();
        throw new Error(`Unknown size at ${entry.name}`);
      }
      mapper.set(entry.offset, entry.value);
    };

    // The original iterated over tables and used .offset values stored in entries
    CustTable.forEach(writeOne);
    AdvTable.forEach(writeOne);
    GpuTable.forEach(writeOne);

    // persist storage to localStorage
    this.storage.save();

    // create download link for patched buffer
    const blob = new Blob([this.buffer], { type: "application/octet-stream" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "loader.kip";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);

    // UI: enable load last saved if needed
    this.toggleLoadLastSavedBtn(true);
  }

  removeHTMLForm() {
    CustTable.forEach(e => e.removeElement());
  }

  toggleLoadLastSavedBtn(visible) {
    const btn = document.getElementById("load_saved");
    if (!btn) return;
    if (visible) {
      btn.addEventListener("click", () => {
        if (this.storage.load()) this.storage.setTable();
      });
      btn.style.removeProperty("display");
      btn.removeAttribute("disabled");
    } else {
      btn.style.setProperty("display", "none");
    }
  }

  createHTMLForm() {
    // create elements for each table entry
    CustTable.forEach(e => e.createElement("config-list-basic"));

    // Add separators/titles for advanced and gpu lists
    const advContainer = document.getElementById("config-list-advanced");
    if (advContainer) {
      const p = document.createElement("p");
      p.innerHTML = "Advanced configuration";
      advContainer.appendChild(p);
    }
    const gpuContainer = document.getElementById("config-list-gpu");
    if (gpuContainer) {
      const p = document.createElement("p");
      p.innerHTML = "Gpu Volt configuration";
      gpuContainer.appendChild(p);
    }

    AdvTable.forEach(e => e.createElement("config-list-advanced"));
    GpuTable.forEach(e => e.createElement("config-list-gpu"));

    // Buttons: load default, load saved, save
    const loadDefaultBtn = document.getElementById("load_default");
    if (loadDefaultBtn) {
      loadDefaultBtn.removeAttribute("disabled");
      loadDefaultBtn.addEventListener("click", () => {
        CustTable.forEach(e => e.setElementDefaultValue());
      });
    }

    // show load saved if we have saved storage
    this.toggleLoadLastSavedBtn(this.storage.load() !== null);

    const saveBtn = document.getElementById("save");
    if (saveBtn) {
      saveBtn.removeAttribute("disabled");
      saveBtn.addEventListener("click", () => {
        try {
          this.save();
        } catch (err) {
          console.error(err);
          alert(String(err));
        }
      });
    }
  }

  initCustTabs() {
    // map nav buttons (role="tablist") to platform toggles
    const tabButtons = Array.from(document.querySelectorAll('nav[role="tablist"] > button, .cust-platform-tabs > button'));
    if (!tabButtons.length) return;
    tabButtons.forEach(btn => {
      btn.removeAttribute("disabled");
      const plat = Number(btn.getAttribute("data-platform"));
      btn.addEventListener("click", (ev) => {
        // style toggling
        const outlineClass = ["outline"];
        btn.classList.remove(...outlineClass);
        tabButtons.filter(x => x !== btn).forEach(x => x.classList.add(...outlineClass));
        // show/hide entries
        CustTable.forEach(e => {
          if (e.isAvailableFor(plat)) e.showElement(); else e.hideElement();
        });
      });
    });
  }

  parse() {
    // beginOffset should already exist
    let offset = this.beginOffset + this.magicLen;
    // read revision (4-byte)
    this.rev = this.mapper[4].get(offset);
    if (this.rev !== CUST_REV_ADV) throw new Error(`Unsupported custRev, expected: ${CUST_REV_ADV}, got ${this.rev}`);
    offset += 4;
    const revEl = document.getElementById("cust_rev");
    if (revEl) revEl.innerHTML = `Cust v${this.rev} is loaded.`;

    const readOne = (entry) => {
      entry.offset = offset;
      const mapper = this.mapper[entry.size];
      if (!mapper) {
        const el = entry.getInputElement();
        if (el) el.focus();
        throw new Error(`Unknown size at ${entry.name}`);
      }
      entry.value = mapper.get(offset);
      offset += entry.size;
      entry.validate();
    };

    CustTable.forEach(readOne);
    AdvTable.forEach(readOne);
    GpuTable.forEach(readOne);
  }

  load(buffer) {
    try {
      this.buffer = buffer;
      this.findMagicOffset();
      this.removeHTMLForm();
      this.parse();
      this.initCustTabs();
      this.createHTMLForm();
    } catch (err) {
      console.error(err);
      alert(String(err));
    }
  }
}

/* ===== Release fetching classes ===== */
class ReleaseAsset {
  constructor(obj) {
    this.downloadUrl = obj?.browser_download_url;
    this.updatedAt = obj?.updated_at;
  }
}

class ReleaseInfo {
  constructor() {
    this.ocLatestApi = "https://api.github.com/repos/Horizon-OC/Horizon-OC/releases/latest";
  }

  async load() {
    try {
      const json = await this.responseFromApi(this.ocLatestApi);
      this.parseOcResponse(json);
    } catch (err) {
      console.error(err);
      alert(String(err));
    }
  }

  async responseFromApi(url) {
    const res = await fetch(url, { method: "GET", headers: { Accept: "application/json" } });
    if (!res.ok) throw new Error(`Failed to connect to "${url}": ${res.status}`);
    return await res.json();
  }

  parseOcResponse(json) {
    this.ocVer = json.tag_name;
    const assets = json.assets || [];
    this.loaderKipAsset = new ReleaseAsset(assets.find(a => a.name.endsWith("hoc.kip")) || {});
    this.sdOutZipAsset = new ReleaseAsset(assets.find(a => a.name.endsWith("dist.zip")) || {});
  }
}

class DownloadSection {
  constructor() {
    this.element = document.getElementById("download_btn_grid") || document.getElementById("download");
  }

  async load() {
    // Wait until the element is visible in the viewport
    for (; !this.isVisible();) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
    const release = new ReleaseInfo();
    await release.load();
    this.update("loader_kip_btn", `hoc.kip <b>${release.ocVer}</b><br>${release.loaderKipAsset.updatedAt}`, release.loaderKipAsset.downloadUrl);
    this.update("sdout_zip_btn", `dist.zip <b>${release.ocVer}</b><br>${release.sdOutZipAsset.updatedAt}`, release.sdOutZipAsset.downloadUrl);
  }

  isVisible() {
    if (!this.element) return true;
    const r = this.element.getBoundingClientRect();
    return r.top > 0 && r.left > 0 && r.bottom - r.height < (window.innerHeight || document.documentElement.clientHeight) && r.right - r.width < (window.innerWidth || document.documentElement.clientWidth);
  }

  update(id, html, href) {
    const el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = html;
    el.removeAttribute("aria-busy");
    if (href) el.setAttribute("href", href);
  }
}

/* ===== Initialization wiring ===== */
document.addEventListener("DOMContentLoaded", async () => {
  // Ensure containers exist (fail gracefully if not)
  const ensureEl = (id, createTag = "div") => {
    if (!document.getElementById(id)) {
      const container = document.createElement(createTag);
      container.id = id;
      container.classList.add("mt-4");
      // append to config section or body as fallback
      const config = document.getElementById("config") || document.body;
      config.appendChild(container);
    }
  };

  ["config-list-basic", "config-list-advanced", "config-list-gpu"].forEach(id => ensureEl(id));

  // Wire file input
  const fileInput = document.getElementById("file");
  if (fileInput) {
    fileInput.addEventListener("change", (ev) => {
      const cust = new Cust();
      const target = ev.target;
      if (!target || !target.files) return;
      const fr = new FileReader();
      fr.readAsArrayBuffer(target.files[0]);
      fr.onloadend = (e) => {
        if (e.target && e.target.readyState === FileReader.DONE) {
          cust.load(e.target.result);
        }
      };
    });
  }

  // Wire DownloadSection (non-blocking)
  (async () => {
    try {
      const ds = new DownloadSection();
      await ds.load();
    } catch (err) {
      console.warn("DownloadSection failed:", err);
    }
  })();

  // If HTML had DOMContentLoaded wiring in original minified code, emulate it:
  // some initialization that original file did on DOMContentLoaded -> start the DownloadSection (done above)
});
