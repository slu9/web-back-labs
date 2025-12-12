function showModal() {
    document.querySelector('div.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function clearErrors() {
    const ids = ['title-ru-error', 'title-error', 'year-error', 'description-error'];
    for (const id of ids) {
        const el = document.getElementById(id);
        if (el) el.innerText = '';
    }
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('title').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    clearErrors();
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;

    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };

    clearErrors();

    const isNew = (id === '' || id === null);
    const url = isNew ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = isNew ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(film)
    })
    .then(resp => resp.json().then(data => ({ ok: resp.ok, data })))
    .then(result => {
        if (!result.ok) {
            const errors = result.data || {};

            if (errors.title_ru && document.getElementById('title-ru-error'))
                document.getElementById('title-ru-error').innerText = errors.title_ru;

            if (errors.title && document.getElementById('title-error'))
                document.getElementById('title-error').innerText = errors.title;

            if (errors.year && document.getElementById('year-error'))
                document.getElementById('year-error').innerText = errors.year;

            if (errors.description && document.getElementById('description-error'))
                document.getElementById('description-error').innerText = errors.description;

            return;
        }

        fillFilmList();
        hideModal();
    })
    .catch(() => {
        if (document.getElementById('description-error')) {
            document.getElementById('description-error').innerText = 'Ошибка запроса к серверу';
        }
    });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(resp => resp.json())
        .then(film => {
            document.getElementById('id').value = film.id; 
            document.getElementById('title').value = film.title || '';
            document.getElementById('title-ru').value = film.title_ru || '';
            document.getElementById('year').value = film.year || '';
            document.getElementById('description').value = film.description || '';
            clearErrors();
            showModal();
        });
}

function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' })
        .then(() => fillFilmList());
}

function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(resp => resp.json())
        .then(films => {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            for (let i = 0; i < films.length; i++) {
                const film = films[i];

                let tr = document.createElement('tr');

                let tdTitleRu = document.createElement('td');    
                let tdTitleOrig = document.createElement('td');   
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                tdTitleRu.innerText = film.title_ru || '';

                const original = film.title || '';
                if (original && original !== film.title_ru) {
                    tdTitleOrig.innerHTML = `<i>(${original})</i>`;
                } else {
                    tdTitleOrig.innerHTML = '';
                }

                tdYear.innerText = film.year || '';

                let editButton = document.createElement('button');
                editButton.innerText = 'редактировать';
                editButton.onclick = function () {
                    editFilm(film.id); 
                };

                let delButton = document.createElement('button');
                delButton.innerText = 'удалить';
                delButton.onclick = function () {
                    deleteFilm(film.id, film.title_ru);
                };

                tdActions.append(editButton);
                tdActions.append(delButton);

                tr.append(tdTitleRu);
                tr.append(tdTitleOrig);
                tr.append(tdYear);
                tr.append(tdActions);

                tbody.append(tr);
            }
        });
}