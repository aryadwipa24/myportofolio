let educationConfig = {};
let educationAbortController;

function initEducations(config) {
    educationConfig = config;

    fetchEducations();
}

function displayPageSection({ showLoading = false, showError = false, showEmpty = false, showGrid = false }) {
    document.getElementById('loading')?.classList.toggle('hide', !showLoading);
    document.getElementById('error')?.classList.toggle('hide', !showError);
    document.getElementById('empty')?.classList.toggle('hide', !showEmpty);
    document.getElementById('grid')?.classList.toggle('hide', !showGrid);
}

function buildEducationItemElement(item) {
    const edu = item.fields;
    const eduId = item.pk;
    const liElement = document.createElement('li');

    const imageHtml = `<img src="${edu.image}" alt="Photo of ${edu.title}">`;

    let starHtml = '';
    if (educationConfig.starUrlPattern) {
        const starUrl = educationConfig.starUrlPattern.replace('00000000-0000-0000-0000-000000000000', eduId);
        const isStarredClass = edu.is_starred ? " is-starred" : "";
        const starText = edu.is_starred ? "Unstar" : "Star";
        const starTitle = edu.star_count > 0 
            ? `Dibintangi oleh ${edu.starred_by_names}` 
            : "Jadilah yang pertama memberi star";

        starHtml = `
            <form method="post" action="${starUrl}" class="star-form" style="display:inline;">
                <input type="hidden" name="csrfmiddlewaretoken" value="${educationConfig.csrfToken}">
                <button type="submit" class="button button-star${isStarredClass}" title="${starTitle}">
                    <span aria-hidden="true">★</span> ${starText}
                    <span class="star-count">${edu.star_count}</span>
                </button>
            </form>
        `;
    }

    liElement.innerHTML = `
        ${imageHtml}
        <div class="education-info">
            <h3>${edu.title}</h3>
            <span>${edu.start} - ${edu.end}</span>
            ${starHtml}
        </div>
    `;

    return liElement;
}

async function fetchEducations() {
    if (educationAbortController) educationAbortController.abort();
    educationAbortController = new AbortController();

    try {
        displayPageSection({ showLoading: true });

        const response = await fetch(educationConfig.endpoint, {
            headers: { 'Accept': 'application/json' },
            signal: educationAbortController.signal,
        });

        if (!response.ok) throw new Error('Failed to fetch education data');
        const educationData = await response.json();

        const listContainer = document.getElementById('grid');

        if (educationData.length === 0) {
            displayPageSection({ showEmpty: true });
        } else {
            listContainer.innerHTML = '';
            educationData.forEach(item => {
                listContainer.appendChild(buildEducationItemElement(item));
            });
            displayPageSection({ showGrid : true });
        }

        renderModalsData(educationData);
    } catch (error) {
        if (error.name === 'AbortError') return;
        console.error('Error loading education:', error);
        displayPageSection({ showError: true });
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

    educationData.forEach(item => {
        const edu = item.fields;
        const eduId = item.pk;

        const checkboxItem = document.createElement('div');
        checkboxItem.className = 'checkbox-item';
        checkboxItem.innerHTML = `
            <input type="checkbox" id="edu-${eduId}" name="selected_educations" value="${eduId}">
            <label for="edu-${eduId}">${edu.title}</label>
        `;
        deleteContainer.appendChild(checkboxItem);

        if (educationConfig.editUrlPattern) {
            const editUrl = educationConfig.editUrlPattern.replace('00000000-0000-0000-0000-000000000000', eduId);
            const editButton = document.createElement('a');
            editButton.href = editUrl;
            editButton.className = 'button button-secondary';
            editButton.textContent = edu.title;
            editContainer.appendChild(editButton);
        }
    });
}