/* ------------------------------------------------------------
   LingoAfrica front‑end logic
   Rules:
   • If “From” = English → “To” can be any Zambian lang (not English)
   • If “From” = a Zambian lang → “To” must be English
   • “From” and “To” can never be identical
------------------------------------------------------------- */

/* -----  language constants  -------------------------------- */
const zamLangs = ["bem", "nya", "swh", "zu", "sn", "nr"];
const LABELS = {
    en:  "🇬🇧 English",
    bem: "🇿🇲 Bemba",
    nya: "🇲🇼 Nyanja",
    swh: "🇰🇪 Swahili",
    zu:  "🇿🇦 Zulu",
    sn:  "🇿🇼 Shona",
    nr:  "🇿🇦 Ndebele",
};

/* DOM elements */
const fromSel   = document.getElementById("from");
const toSel     = document.getElementById("to");
const translateBtn = document.getElementById("translateBtn");
const copyBtn   = document.getElementById("copyBtn");
const shareBtn  = document.getElementById("shareBtn");
const sourceTA  = document.getElementById("source");
const targetTA  = document.getElementById("target");

/* -----  helpers  ------------------------------------------ */
function makeOption(code) {
    const opt = document.createElement("option");
    opt.value = code;
    opt.textContent = LABELS[code];
    return opt;
}

function rebuildToDropdown() {
    const fromVal = fromSel.value;
    toSel.innerHTML = "";                            // clear current list

    if (fromVal === "en") {
        zamLangs.forEach(c => toSel.appendChild(makeOption(c)));
        toSel.selectedIndex = 0;                     // pick first by default
    } else {
        toSel.appendChild(makeOption("en"));
        toSel.value = "en";
    }
}

function getRoute() {
    const f = fromSel.value;
    const t = toSel.value;
    return (f === t) ? null : `${f}_${t}`;
}

/* -----  main translate action  ----------------------------- */
async function translate() {
    const text = sourceTA.value.trim();
    if (!text) return;

    const route = getRoute();
    if (!route) {
        alert("Please choose different languages for From and To.");
        return;
    }

    translateBtn.disabled = true;
    translateBtn.textContent = "Translating…";

    try {
        const res = await fetch("/translate", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({route, text})
        });
        const data = await res.json();
        targetTA.value = data.translation ?? `[error: ${data.error}]`;
    } catch {
        targetTA.value = "[network error]";
    } finally {
        translateBtn.disabled = false;
        translateBtn.textContent = "Translate ✨";
    }
}

/* -----  init listeners  ----------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
    rebuildToDropdown();                 // set initial “To” list
    fromSel.addEventListener("change", rebuildToDropdown);
    translateBtn.addEventListener("click", translate);

    copyBtn.addEventListener("click", () =>
        navigator.clipboard.writeText(targetTA.value));

    shareBtn.addEventListener("click", async () => {
        const text = targetTA.value;
        if (navigator.share) {
            await navigator.share({text});
        } else {
            alert("Sharing not supported—copied to clipboard instead.");
            navigator.clipboard.writeText(text);
        }
    });

    /* ----------  toast feedback  ---------- */
    function showToast(msg){
        const t = document.getElementById("toast");
        t.textContent = msg;
        t.classList.add("show");
        setTimeout(()=>t.classList.remove("show"), 2000);
    }

    /* Patch existing handlers */
    copyBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(targetTA.value);
        showToast("Translation copied!");
    });

    shareBtn.addEventListener("click", async () => {
        const text = targetTA.value;
        if (navigator.share) {
            await navigator.share({text});
        } else {
            navigator.clipboard.writeText(text);
            showToast("Copied to clipboard!");
        }
    });

    /* Fun fact banner */
    const facts = [
        "Bemba has borrowed many loanwords from Swahili and English.",
        "Nyanja is mutually intelligible with Chichewa, spoken in Malawi.",
        "The Zulu word for ‘hello’ is ‘Sawubona’ (literally “I see you”)."
    ];
    document.getElementById("funFact").textContent =
        "💡 Fun fact: " + facts[Math.floor(Math.random()*facts.length)];
});
