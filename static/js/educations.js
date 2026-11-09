let educationConfig = {};
let educationAbortController;

function initEducations(config) {
    educationConfig = config;
    setupAddEducationHandler();

    const grid = document.getElementById('grid');
    if (grid) {
        grid.addEventListener('click', async function(event) {
            const button = event.target.closest('button[data-action="star"]');
            if (!button || button.disabled) return;

            button.disabled = true;
            try {
                const url = educationEndpoint(educationConfig.starUrlPattern, button.dataset.id);
                await writeEducation(url, 'POST');
                notifyEducation('Berhasil', 'Star berhasil diperbarui.', 'success');
                await fetchEducations();
            } catch (error) {
                notifyEducation('Gagal mengubah star', error.message, 'error');
            } finally {
                button.disabled = false;
            }
        });
    }

    const deleteForm = document.getElementById('delete-checkbox-list')?.closest('form');
    if (deleteForm) {
        deleteForm.addEventListener('submit', deleteEducations);
    }

    fetchEducations();
}

function educationEndpoint(pattern, id) {
    return pattern.replace('00000000-0000-0000-0000-000000000000', id);
}

function notifyEducation(title, message, type) {
    if (typeof showToast === 'function') {
        showToast(title, message, type);
    } else {
        window.alert(`${title}: ${message}`);
    }
}

function displayPageSection({ showLoading = false, showError = false, showEmpty = false, showGrid = false }) {
    document.getElementById('loading')?.classList.toggle('hide', !showLoading);
    document.getElementById('error')?.classList.toggle('hide', !showError);
    document.getElementById('empty')?.classList.toggle('hide', !showEmpty);
    document.getElementById('grid')?.classList.toggle('hide', !showGrid);
}

function escapeHtml(value) {
    return String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

function apiErrorMessage(data, status) {
    if (typeof data === 'string') return data;
    const messages = Object.entries(data || {}).flatMap(([field, errors]) => {
        const values = Array.isArray(errors) ? errors : [errors];
        return values.map(value => {
            if (typeof value !== 'string') return JSON.stringify(value);
            return ['detail', 'non_field_errors'].includes(field)
                ? value : `${field}: ${value}`;
        });
    });
    return messages.join(' ') || `Permintaan gagal (HTTP ${status}).`;
}

function buildEducationItemElement(item) {
    const liElement = document.createElement('li');

    const imageHtml = item.image ? `<img src="${escapeHtml(item.image)}"
                                   alt="Photo of ${escapeHtml(item.title)}">`
                                : `<img src="/static/img/no-image.png"
                                   alt="No image">`;

    const starHtml = educationConfig.isAuthenticated
        ? `<button type="button"
                class="button button-star${item.is_starred ? ' is-starred' : ''}"
                data-action="star"
                data-id="${escapeHtml(item.id)}"
                title="${escapeHtml(item.starred_by_names)}">
            ★ ${item.is_starred ? 'Unstar' : 'Star'}
            <span class="star-count">${item.star_count}</span>
        </button>`
        :  `<a href="/login" class="button">
                ★ Star <span class="star-count">${item.star_count}</span>
            </a>`;

    liElement.innerHTML = `
        ${imageHtml}
        <div class="education-info">
            <h3>${escapeHtml(item.title)}</h3>
            <span>${escapeHtml(formatEducationDate(item.start))} - ${escapeHtml(formatEducationDate(item.end))}</span>
            ${starHtml}
        </div>
    `;

    return liElement;
}

function formatEducationDate(value) {
    if (!value) return 'Present';
    const [year, month] = String(value).split('-').map(Number);
    const date = new Date(year, month - 1, 1);
    return Number.isNaN(date.getTime())
        ? String(value)
        : date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
}

function closeEducationModal() {
    document.getElementById("add-education-modal").hidePopover();
}

async function fetchEducations() {
    if (educationAbortController) educationAbortController.abort();
    educationAbortController = new AbortController();

    try {
        displayPageSection({ showLoading: true });

        const url = new URL(educationConfig.endpoint, window.location.origin);

        const response = await fetch(url, {headers: { Accept: 'application/json' }, signal: educationAbortController.signal,});

        const educationData = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(apiErrorMessage(educationData, response.status));
        }

        const listContainer = document.getElementById('grid');

        listContainer.replaceChildren(
            ...educationData.map(buildEducationItemElement)
        );

        displayPageSection({
            showGrid: educationData.length > 0,
            showEmpty: educationData.length === 0,
        });

        renderModalsData(educationData);

    } catch (error) {
        if (error.name === 'AbortError') return;

        displayPageSection({ showError: true });
        notifyEducation('Gagal memuat pendidikan', error.message, 'error');
    }
}

function renderModalsData(educationData) {
    const deleteContainer = document.getElementById('delete-checkbox-list');
    const editContainer = document.getElementById('edit-select-list');

    if (!deleteContainer || !editContainer) return;

    if (educationData.length === 0) {
        deleteContainer.innerHTML = '<p>Tidak ada data untuk dihapus.</p>';
        editContainer.innerHTML = '<p>Belum ada data untuk diubah.</p>';
        return;
    }

    deleteContainer.innerHTML = '';
    editContainer.innerHTML = '';

    educationData.forEach(edu => {
        if (deleteContainer && educationConfig.isSuperuser) {
            const checkboxItem = document.createElement('div');
            checkboxItem.className = 'checkbox-item';

            checkboxItem.innerHTML = `
                <input type="checkbox"
                    id="edu-${escapeHtml(edu.id)}"
                    name="selected_educations"
                    value="${escapeHtml(edu.id)}">
                <label for="edu-${escapeHtml(edu.id)}">
                    ${escapeHtml(edu.title)}
                </label>
            `;

            deleteContainer.appendChild(checkboxItem);
        }

        if (editContainer &&
            (educationConfig.isSuperuser || educationConfig.isEditor)) {

            const editButton = document.createElement('a');
            editButton.href = educationEndpoint(
                educationConfig.editUrlPattern, edu.id
            );
            editButton.className = 'button button-secondary';
            editButton.textContent = edu.title;

            editContainer.appendChild(editButton);
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setupAddEducationHandler() {
    const educationForm = document.getElementById('education-form');
    if (educationForm) {
        educationForm.addEventListener('submit', addEducation);
    }
}

async function addEducation(event) {
    event.preventDefault();

    const educationForm = event.target;
    const submitButton = educationForm.querySelector('button[type="submit"]');

    if (submitButton) submitButton.disabled = true;

    try {
        const payload = new FormData(educationForm);
        const start = payload.get('start');
        const end = payload.get('end');

        if (start) {
            payload.set('start', `${start}-01`);
        }

        if (end) {
            payload.set('end', `${end}-01`);
        } else {
            payload.delete('end');
        }
        const imageInput = educationForm.querySelector('input[name="image"]');

        if (!imageInput?.files.length) {
            payload.delete('image');
        }

        await writeEducation(educationConfig.endpoint, 'POST', payload);

        educationForm.reset();
        document.getElementById('add-education-modal')?.hidePopover();

        notifyEducation(
            'Berhasil',
            'Pendidikan baru berhasil ditambahkan!',
            'success'
        );

        await fetchEducations();

    } catch (error) {
        notifyEducation(
            'Gagal menambahkan pendidikan',
            error.message,
            'error'
        );
    } finally {
        if (submitButton) submitButton.disabled = false;
    }
}

async function writeEducation(url, method, payload) {
    const headers = {
        Accept: 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
            || educationConfig.csrfToken
            || document.querySelector(
                'input[name="csrfmiddlewaretoken"]'
            )?.value
            || '',
    };

    const options = { method, headers };

    if (payload instanceof FormData) {
        options.body = payload;
    } else if (payload !== undefined) {
        headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(payload);
    }

    const response = await fetch(url, options);

    const data = response.status === 204
        ? null
        : await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(apiErrorMessage(data, response.status));
    }

    return data;
}

async function deleteEducations(event) {
    event.preventDefault();
    const selectedIds = [...document.querySelectorAll(
        '#delete-checkbox-list input[name="selected_educations"]:checked'
    )].map(input => input.value);

    if (selectedIds.length === 0) {
        notifyEducation('Belum ada pilihan', 'Pilih pendidikan yang ingin dihapus.', 'error');
        return;
    }

    const button = event.submitter || event.target.querySelector('button[type="submit"]');
    if (button) button.disabled = true;

    let deleted = 0;
    try {
        for (const id of selectedIds) {
            await writeEducation(
                educationEndpoint(educationConfig.detailUrlPattern, id),
                'DELETE'
            );
            deleted++;
        }
        document.getElementById('delete-education')?.hidePopover();
        notifyEducation('Berhasil', `${deleted} riwayat pendidikan dihapus.`, 'success');
    } catch (error) {
        notifyEducation('Gagal menghapus', `${deleted} berhasil dihapus. ${error.message}`, 'error');
    } finally {
        if (button) button.disabled = false;
        await fetchEducations();
    }
}