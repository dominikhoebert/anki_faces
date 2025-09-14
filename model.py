import genanki
from random import randrange

my_model = genanki.Model(
    randrange(1 << 30, 1 << 31),
    'AllInOne (kprim, mc, sc)',
    fields=[
        {'name': 'Question'},
        {'name': 'Title'},
        {'name': 'QType (0=kprim,1=mc,2=sc)'},
        {'name': 'Q_1'},
        {'name': 'Q_2'},
        {'name': 'Q_3'},
        {'name': 'Q_4'},
        {'name': 'Q_5'},
        {'name': 'Answers'},
        {'name': 'Sources'},
        {'name': 'Extra 1'},
    ],
    templates=[
        {
            'name': 'AllInOne (kprim, mc, sc)',
            'qfmt': """<script>
    // Loading Persistence
    // https://github.com/SimonLammer/anki-persistence
    // v0.5.2 - https://github.com/SimonLammer/anki-persistence/blob/62463a7f63e79ce12f7a622a8ca0beb4c1c5d556/script.js
    if (void 0 === window.Persistence) { var _persistenceKey = "github.com/SimonLammer/anki-persistence/", _defaultKey = "_default"; if (window.Persistence_sessionStorage = function () { var e = !1; try { "object" == typeof window.sessionStorage && (e = !0, this.clear = function () { for (var e = 0; e < sessionStorage.length; e++) { var t = sessionStorage.key(e); 0 == t.indexOf(_persistenceKey) && (sessionStorage.removeItem(t), e--) } }, this.setItem = function (e, t) { void 0 == t && (t = e, e = _defaultKey), sessionStorage.setItem(_persistenceKey + e, JSON.stringify(t)) }, this.getItem = function (e) { return void 0 == e && (e = _defaultKey), JSON.parse(sessionStorage.getItem(_persistenceKey + e)) }, this.removeItem = function (e) { void 0 == e && (e = _defaultKey), sessionStorage.removeItem(_persistenceKey + e) }) } catch (e) { } this.isAvailable = function () { return e } }, window.Persistence_windowKey = function (e) { var t = window[e], i = !1; "object" == typeof t && (i = !0, this.clear = function () { t[_persistenceKey] = {} }, this.setItem = function (e, i) { void 0 == i && (i = e, e = _defaultKey), t[_persistenceKey][e] = i }, this.getItem = function (e) { return void 0 == e && (e = _defaultKey), t[_persistenceKey][e] || null }, this.removeItem = function (e) { void 0 == e && (e = _defaultKey), delete t[_persistenceKey][e] }, void 0 == t[_persistenceKey] && this.clear()), this.isAvailable = function () { return i } }, window.Persistence = new Persistence_sessionStorage, Persistence.isAvailable() || (window.Persistence = new Persistence_windowKey("py")), !Persistence.isAvailable()) { var titleStartIndex = window.location.toString().indexOf("title"), titleContentIndex = window.location.toString().indexOf("main", titleStartIndex); titleStartIndex > 0 && titleContentIndex > 0 && titleContentIndex - titleStartIndex < 10 && (window.Persistence = new Persistence_windowKey("qt")) } }
</script>

{{#Title}}<h3 id="myH1">{{Title}}</h3>{{/Title}}
{{#Question}}<p>{{Question}}</p>{{/Question}}

<div class="tappable">
    <table style="border: 1px solid black" id="qtable"></table>
</div>

<div class="hidden" id="Q_solutions">{{Answers}}</div>
<div class="hidden" id="Card_Type">{{QType (0=kprim,1=mc,2=sc)}}</div>

<div class="hidden" id="Q_1">{{Q_1}}</div>
<div class="hidden" id="Q_2">{{Q_2}}</div>
<div class="hidden" id="Q_3">{{Q_3}}</div>
<div class="hidden" id="Q_4">{{Q_4}}</div>
<div class="hidden" id="Q_5">{{Q_5}}</div>

<script>
    // Generate the table depending on the type.
    function generateTable() {

        // Options are modified according to user's meta.json in the addon's folder
        const OPTIONS = {
    maxQuestionsToShow: 0
};


        var type = document.getElementById("Card_Type").innerHTML;
        var table = document.createElement("table");
        var tbody = document.createElement("tbody");

        if (type == 0) {
            tbody.innerHTML = '<tr><th>yes</th><th>no</th><th></th></tr>';
        }

        stripHtmlTagsFromSolutionString();

        let solutions = getCorrectAnswers();
        let questionTableHtmlLinesToSolution = []
        for (var i = 0; true; i++) {
            if (document.getElementById('Q_' + (i + 1)) != undefined) {
                if (document.getElementById('Q_' + (i + 1)).innerHTML != '') {
                    var html = [];

                    let answerText = document.getElementById('Q_' + (i + 1)).innerHTML;
                    let labelTag = (type == 0) ? '' :
                        '<label for="inputQuestion' + (i + 1) + '">' + answerText + '</label>';
                    let textAlign = (type == 0) ? 'center' : 'left';

                    html.push('<tr>');
                    var maxColumns = ((type == 0) ? 2 : 1);
                    for (var j = 0; j < maxColumns; j++) {
                        let inputTag = '<input id="inputQuestion' + (i + 1) +
                            '" name="ans_' + ((type != 2) ? (i + 1) : 'A') +
                            '" type="' + ((type == 1) ? 'checkbox' : 'radio') +
                            // TODO: I don't see how these values are used, please add a comment
                            '" value="' + ((j == 0) ? 1 : 0) + '">';
                        html.push(
                            '<td onInput="onCheck()" style="text-align: ' + textAlign + '">' + inputTag +
                            labelTag +
                            '</td>');
                    }
                    if (type == 0) {
                        html.push('<td>' + answerText + '</td>');
                    }
                    html.push('</tr>');

                    questionTableHtmlLinesToSolution.push({
                        html: html.join(""),
                        solution: solutions[i]
                    });
                }
            } else {
                break;
            }
        }
        let shuffledQuestionTableHtmlLinesToSolution = getShuffledQuestionTableHtmlLinesToSolution(
            questionTableHtmlLinesToSolution, type, OPTIONS['maxQuestionsToShow']);

        let shuffledHtmlLines = shuffledQuestionTableHtmlLinesToSolution
            .map(o => o.html)
            .join("");
        let shuffledSolutions = shuffledQuestionTableHtmlLinesToSolution
            .map(o => o.solution);

        tbody.innerHTML += shuffledHtmlLines;

        table.appendChild(tbody);
        document.getElementById('qtable').innerHTML = table.innerHTML;

        storeCorrectAnswersInHtml(shuffledSolutions)

        onCheck();  // store user answers at least once in case nothing was ticked
    }

    function stripHtmlTagsFromSolutionString() {
        let solutionString = document.getElementById("Q_solutions").innerHTML;
        document.getElementById("Q_solutions").innerHTML = solutionString.replace(/(<([^>]+)>)/gi, "");
    }

    /**
     * Returns the shuffled and potentially reduced lines of HTML combined with their solution value
     *
     * In case of single choice it is guaranteed that the correct answer is shuffled in
     * between the wrong ones.
     *
     * @param   {questionTableHtmlLinesToSolution}  Array[Object]   objects containing the
     *                                                              properties 'html' and 'solution'
     * @param   {type}                              int             Card type
     * @param   {maxQuestionsToShow}                int             see config options
     */
    function getShuffledQuestionTableHtmlLinesToSolution(
        questionTableHtmlLinesToSolution, type, maxQuestionsToShow) {

        if (type != 2) {
            shuffledQuestionTableHtmlLinesToSolution = questionTableHtmlLinesToSolution.sort(
                () => Math.random() < 0.5 ? -1 : 1);

            if (maxQuestionsToShow > 1) {
                return shuffledQuestionTableHtmlLinesToSolution.slice(0, maxQuestionsToShow);
            } else {
                return shuffledQuestionTableHtmlLinesToSolution;
            }

        } else {
            // To have the single correct answer randomly inserted into the wrong ones
            let correctAnswer = questionTableHtmlLinesToSolution.find(o => o.solution == 1);
            let wrongAnswers = questionTableHtmlLinesToSolution.filter(o => o.solution == 0);
            wrongAnswers.sort(() => Math.random() < 0.5 ? -1 : 1);

            if (maxQuestionsToShow > 1) {
                wrongAnswers = wrongAnswers.slice(0, maxQuestionsToShow - 1);
            }

            let randomIndex = Math.floor(Math.random() * (wrongAnswers.length + 1));
            wrongAnswers.splice(randomIndex, 0, correctAnswer);

            return wrongAnswers;
        }
    }

    /**
     * Returns true if the option box/circle is checked.
     *
     * In case of kprim the second box is used as reference.
     *
     * @param   {HTMLTableRowElement}    optionRow    Row containing option boxes/circles.
     * @param   {number}    index   Index of the option in question.
     */
    function isOptionChecked(optionRow, index) {
        return optionRow.getElementsByTagName("td")[index].getElementsByTagName("input")[0].checked
    }

    function getUserAnswers() {
        let type = document.getElementById("Card_Type").innerHTML;
        let qrows = document.getElementById("qtable").getElementsByTagName('tbody')[0].getElementsByTagName("tr");
        let userAnswers = [];
        for (let i = 0; i < qrows.length; i++) {
            if (type == 0 && i == 0) {
                i++; // to skip the first row containing no checkboxes when type is 'kprim'
            }
            if (type == 0) {
                if (isOptionChecked(qrows[i], 0)) {
                    userAnswers.push(1);
                } else if (isOptionChecked(qrows[i], 1)) {
                    userAnswers.push(0);
                } else {
                    userAnswers.push(2);
                }
            } else {
                if (isOptionChecked(qrows[i], 0)) {
                    userAnswers.push(1);
                } else {
                    userAnswers.push(0);
                }
            }
        }
        return userAnswers
    }

    /**
     * Get the solutions stored in the hidden div with id "Q_solutions" as Array.
     */
    function getCorrectAnswers() {
        let solutions = document.getElementById("Q_solutions").innerHTML.split(" ").map(string => Number(string));

        return solutions;
    }

    function storeCorrectAnswersInHtml(solutions) {
        document.getElementById("Q_solutions").innerHTML = solutions.join(" ");
    }

    /**
     * On checking an option this collects and stores answers in between front/back of the card.
     *
     * In case of kprim only the first box is looked at, if it isn't checked the second box has to be.
     * By default a '1' in the answers stands for 'yes' which is the first option from the left.
     */
    function onCheck() {
        // Send question table and encoded answers to Persistence along with the provided solutions
        if (Persistence.isAvailable()) {
            Persistence.clear();
            Persistence.setItem('user_answers', getUserAnswers());
            Persistence.setItem('Q_solutions', getCorrectAnswers());
            Persistence.setItem('qtable', document.getElementById("qtable").innerHTML);
        }
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function tickCheckboxOnNumberKeyDown(event) {
        const keyName = event.key;

        let tableBody = document.getElementById("qtable").getElementsByTagName('tbody')[0];
        var tableRows = tableBody.getElementsByTagName("tr");

        if (0 < +keyName && +keyName < 10) {
            let tableData = tableRows[+keyName - 1].getElementsByTagName("td")[0];
            let tableRow = tableData.getElementsByTagName("input")[0];
            tableRow.checked = !tableRow.checked;
            onCheck();
        }
    }

    // addCheckboxTickingShortcuts is an easy approach on using only the keyboard to toggle checkboxes in mc/sc.
    //
    // Naturally the number keys are an intuitive choice here. Unfortunately anki does capture those.
    // So the workaround is to hold the (left) 'Alt' key and then type the corresponding number to toggle the row.
    function addCheckboxTickingShortcuts() {
        document.addEventListener('keydown', tickCheckboxOnNumberKeyDown, false);
    }

    function isMobile() {
        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            return true;
        } else {
            return false;
        }
    }

    function run() {
        // for previewing the cards in "Manage Note Type..."
        let DEFAULT_CARD_TYPE = 1;
        let DEFAULT_SOLUTIONS = "1 0 0 0 0";

        if (isNaN(document.getElementById("Card_Type").innerHTML)) {
            document.getElementById("Card_Type").innerHTML = DEFAULT_CARD_TYPE;
        }
        if ('{' + '{Answers}' + '}' == document.getElementById("Q_solutions").innerHTML) {
            document.getElementById("Q_solutions").innerHTML = DEFAULT_SOLUTIONS;
        }

        if (document.getElementById("Card_Type").innerHTML != 0 && !isMobile()) {
            addCheckboxTickingShortcuts();
        }

        setTimeout(generateTable(), 1);
    }

    async function waitForReadyStateAndRun() {
        for (let i = 0; i < 100; i++) {
            if (document.readyState === "complete") {
                run();
                break;
            }
            console.log("Document not yet fully loaded (readyState: " + document.readyState + "). Retry in 0.1s.");
            await sleep(100);
        }
    }

    /*
    The following block is inspired by Glutanimate's Cloze Overlapper card template.
    The Cloze Overlapper card template is licensed under the CC BY-SA 4.0
    license (https://creativecommons.org/licenses/by-sa/4.0/).
    */
    if (document.readyState === "complete") {
        run();
    } else {
        waitForReadyStateAndRun();
    }
</script>
""",
            'afmt': """<script>
    // Loading Persistence
    // https://github.com/SimonLammer/anki-persistence
    // v0.5.2 - https://github.com/SimonLammer/anki-persistence/blob/62463a7f63e79ce12f7a622a8ca0beb4c1c5d556/script.js
    if (void 0 === window.Persistence) { var _persistenceKey = "github.com/SimonLammer/anki-persistence/", _defaultKey = "_default"; if (window.Persistence_sessionStorage = function () { var e = !1; try { "object" == typeof window.sessionStorage && (e = !0, this.clear = function () { for (var e = 0; e < sessionStorage.length; e++) { var t = sessionStorage.key(e); 0 == t.indexOf(_persistenceKey) && (sessionStorage.removeItem(t), e--) } }, this.setItem = function (e, t) { void 0 == t && (t = e, e = _defaultKey), sessionStorage.setItem(_persistenceKey + e, JSON.stringify(t)) }, this.getItem = function (e) { return void 0 == e && (e = _defaultKey), JSON.parse(sessionStorage.getItem(_persistenceKey + e)) }, this.removeItem = function (e) { void 0 == e && (e = _defaultKey), sessionStorage.removeItem(_persistenceKey + e) }) } catch (e) { } this.isAvailable = function () { return e } }, window.Persistence_windowKey = function (e) { var t = window[e], i = !1; "object" == typeof t && (i = !0, this.clear = function () { t[_persistenceKey] = {} }, this.setItem = function (e, i) { void 0 == i && (i = e, e = _defaultKey), t[_persistenceKey][e] = i }, this.getItem = function (e) { return void 0 == e && (e = _defaultKey), t[_persistenceKey][e] || null }, this.removeItem = function (e) { void 0 == e && (e = _defaultKey), delete t[_persistenceKey][e] }, void 0 == t[_persistenceKey] && this.clear()), this.isAvailable = function () { return i } }, window.Persistence = new Persistence_sessionStorage, Persistence.isAvailable() || (window.Persistence = new Persistence_windowKey("py")), !Persistence.isAvailable()) { var titleStartIndex = window.location.toString().indexOf("title"), titleContentIndex = window.location.toString().indexOf("main", titleStartIndex); titleStartIndex > 0 && titleContentIndex > 0 && titleContentIndex - titleStartIndex < 10 && (window.Persistence = new Persistence_windowKey("qt")) } }
</script>

{{#Title}}<h3 id="myH1">{{Title}}</h3>{{/Title}}
{{#Question}}<p>{{Question}}</p>{{/Question}}
<table id="qtable"></table>
<p id="output"></p>
<div class="hidden" id="MC_solutions">solutions_here</div>
<div class="hidden" id="user_answers">user_answers_here</div>
<div class="hidden" id="CardType">{{QType (0=kprim,1=mc,2=sc)}}</div>
<p id="canswerresult"><b>Correct answers: x %</b></p>
{{#Sources}}<p class="small" id="sources"><b>Sources:</b><br />{{Sources}}</p>{{/Sources}}
{{#Extra 1}}<p class="small" id="extra1"><b>Extra 1:</b><br />{{Extra 1}}</p>{{/Extra 1}}

<script>
    "use strict";

    function onLoad() {
        // Check if Persistence is recognized to prevent errors when viewing note in "Manage Note Types..."
        if (Persistence.isAvailable && Persistence.getItem('Q_solutions') !== null) {

            const DEFAULT_COLORING = { // Defines which class should be set
                wrongAndNotTicked: 'correct',
                correctAndTicked: 'correct',
                wrongButTicked: 'wrong',
                correctButNotTicked: 'wrong',
                withoutSelection: "wrong" // Kprim was marked neither correct nor wrong
            };

            const ALTERNATE_COLORING = { // Defines which class should be set
                wrongAndNotTicked: '',
                correctAndTicked: '',
                wrongButTicked: 'wrong',
                correctButNotTicked: 'correct',
                withoutSelection: "wrong" // Kprim was marked neither correct nor wrong
            };

            // Options are modified according to user's meta.json in the addon's folder
            const OPTIONS = {
    qtable: {
        visible: true,
        colorize: false,
        colors: ALTERNATE_COLORING
    },
    atable: {
        visible: true,
        colorize: true,
        colors: ALTERNATE_COLORING
    }
};


            const colorizeTableRow = function (row, tableType, solution, answer) {
                let colorOptions = OPTIONS[tableType].colors

                if ((solution === 1) && (answer === 1)) {
                    row.setAttribute("class", colorOptions.correctAndTicked);
                } else if ((solution === 0) && (answer === 0)) {
                    row.setAttribute("class", colorOptions.wrongAndNotTicked);
                } else if ((solution === 0) && (answer === 1)) {
                    row.setAttribute("class", colorOptions.wrongButTicked);
                } else if ((solution === 1) && (answer === 0)) {
                    row.setAttribute("class", colorOptions.correctButNotTicked);
                } else if (type == 0 && (answer === 2)) {
                    row.setAttribute("class", colorOptions.withoutSelection);
                }
            }

            // Parsing solutions
            var solutions = Persistence.getItem('Q_solutions');
            var answers = Persistence.getItem('user_answers');

            var type = document.getElementById('CardType').innerHTML;
            var qtable = document.getElementById('qtable');
            qtable.innerHTML = Persistence.getItem('qtable');

            // Clone atable from qtable before colorizing the qtable
            if (OPTIONS.atable.visible) {
                var output = document.getElementById("output");
                var atable = qtable.cloneNode(true);
                atable.setAttribute("id", "atable");
                output.innerHTML = "<hr id='answer' />" + atable.outerHTML;

                var arows = document.getElementById("atable").getElementsByTagName("tbody")[0].getElementsByTagName("tr");
            }

            if (OPTIONS.qtable.visible) {
                var qrows = qtable.getElementsByTagName('tbody')[0].getElementsByTagName("tr");
                for (let i = 0; i < answers.length; i++) {
                    //Set the radio buttons in the qtable.
                    if (type == 0) {
                        if (answers[i] === 1) {
                            let radioButton = qrows[i + 1].getElementsByTagName("td")[0].getElementsByTagName("input")[0];
                            radioButton.checked = true;
                            radioButton.disabled = true;
                        } else if (answers[i] === 0) {
                            let radioButton = qrows[i + 1].getElementsByTagName("td")[1].getElementsByTagName("input")[0];
                            radioButton.checked = true;
                            radioButton.disabled = true;
                        }
                    } else {
                        let radioButton = qrows[i].getElementsByTagName("td")[0].getElementsByTagName("input")[0];
                        radioButton.checked = (answers[i] === 1) ? true : false;
                        radioButton.disabled = true;
                    }
                    //Colorize the qtable.
                    if (OPTIONS.qtable.colorize) {
                        colorizeTableRow(qrows[(type != 0) ? i : i + 1], "qtable", solutions[i], answers[i]);
                    }
                }
            } else qtable.innerHTML = ""

            var canswers = 0;
            for (let i = 0; i < solutions.length; i++) {
                if (OPTIONS.atable.visible) {
                    //Rename the radio buttons of the atable to avoid interference with those in the qtable.
                    if (type == 0) arows[i + 1].getElementsByTagName("td")[1].getElementsByTagName("input")[0].setAttribute("name", "ans_" + ((type != 2) ? String(i + 1) : 'A') + "_solution");
                    arows[(type != 0) ? i : i + 1].getElementsByTagName("td")[0].getElementsByTagName("input")[0].setAttribute("name", "ans_" + ((type != 2) ? String(i + 1) : 'A') + "_solution");
                    //Set the radio buttons in the atable.
                    if (type == 0) {
                        let radioButton = arows[i + 1].getElementsByTagName("td")[solutions[i] ? 0 : 1].getElementsByTagName("input")[0];
                        radioButton.checked = true;
                        radioButton.disabled = true;
                    }
                    else {
                        let radioButton = arows[i].getElementsByTagName("td")[0].getElementsByTagName("input")[0];
                        radioButton.checked = solutions[i] ? true : false;
                        radioButton.disabled = true;
                    }
                    //Colorize the atable.
                    if (OPTIONS.atable.colorize) {
                        colorizeTableRow(arows[(type != 0) ? i : i + 1], "atable", solutions[i], answers[i]);
                    }
                }

                //Count correct answers.
                if (solutions[i] && answers[i] === 1) {
                    canswers = canswers + 1;
                } else if (!solutions[i] && answers[i] === 0) {
                    canswers = canswers + 1;
                }
            }
        }
        var canswerresult = document.getElementById("canswerresult");
        if (type == 2) {
            canswerresult.innerHTML = "<b>" + ((canswers / solutions.length == 1) ? "Correct.</b>" : "Nope.</b>");
        } else {
            canswerresult.innerHTML = "<b>Correct answers: " + Math.round(canswers / solutions.length * 100) + " %</b>";
        }

        Persistence.clear();
    }

    function isMobile() {
        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            return true;
        } else {
            return false;
        }
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function run() {
        if (!isMobile() && typeof tickCheckboxOnNumberKeyDown !== "undefined") {
            // To make sure there isn't a previously registered event handler lingering into the next review
            document.removeEventListener('keydown', tickCheckboxOnNumberKeyDown, false);
        }
        setTimeout(onLoad(), 1);
    }

    async function waitForReadyStateAndRun() {
        for (let i = 0; i < 100; i++) {
            if (document.readyState === "complete") {
                run();
                break;
            }
            console.log("Document not yet fully loaded (readyState: " + document.readyState + "). Retry in 0.1s.");
            await sleep(100);
        }
    }

    /*
    The following block is inspired by Glutanimate's Cloze Overlapper card template.
    The Cloze Overlapper card template is licensed under the CC BY-SA 4.0
    license (https://creativecommons.org/licenses/by-sa/4.0/).
    */
    if (document.readyState === "complete") {
        run();
    } else if (isMobile()) {
        document.addEventListener("DOMContentLoaded", function () {
            setTimeout(onLoad, 1);
        }, false);
    } else {
        waitForReadyStateAndRun();
    }
</script>
""",
        },
    ],
    css=""".card {
  font-family: arial;
  font-size: 20px;
  text-align: center;
  color: black;
  background-color: white;
}

.small {
  font-size: 15px;
}

table, td, th {
  border-collapse: collapse;
  padding: 5px;
}

table {
  display: inline-block;
  text-align: left;
}

label {
  display: inline-block;
  vertical-align: middle;
  margin-left: 0.4em;
}

.correct {
  background-color: lime;
}

.nightMode .correct {
  background-color: #009900;
}

.wrong {
  background-color: OrangeRed;
}

.hidden {
  /*
  This block is from Glutanimate's Cloze Overlapper card template.
  The Cloze Overlapper card template is licensed under the CC BY-SA 4.0
  license (https://creativecommons.org/licenses/by-sa/4.0/).
  */
  /* guarantees a consistent width across front and back */
  font-weight: bold;
  display: block;
  line-height: 0;
  height: 0;
  overflow: hidden;
  visibility: hidden;
}
""")
