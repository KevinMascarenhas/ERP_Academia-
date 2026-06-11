const API_BASE = "";

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function request(method, path, body = null, csrfToken = null) {
    const headers = {
        "Accept": "application/json",
    };

    if (body !== null) {
        headers["Content-Type"] = "application/json";
    }

    if (csrfToken) {
        headers["X-CSRFToken"] = csrfToken;
    }

    const options = {
        method,
        headers,
        credentials: "same-origin",
    };

    if (body !== null) {
        options.body = JSON.stringify(body);
    }

    let response;
    try {
        response = await fetch(`${API_BASE}${path}`, options);
    } catch {
        throw new Error("Servidor indisponível. Verifique se o backend está rodando.");
    }

    if (response.status === 204) {
        return null;
    }

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(formatError(data, response.status));
    }

    return data;
}

const api = {
    get: path => request("GET", path),
    post: (path, body, csrfToken) => request("POST", path, body, csrfToken),
    put: (path, body, csrfToken) => request("PUT", path, body, csrfToken),
    patch: (path, body, csrfToken) => request("PATCH", path, body, csrfToken),
    del: (path, csrfToken) => request("DELETE", path, null, csrfToken),
};

function formatError(data, statusCode) {
    if (Array.isArray(data?.detail)) {
        return data.detail.map(item => item.msg || item).join(", ");
    }

    if (data?.detail) {
        return data.detail;
    }

    if (typeof data === "object" && Object.keys(data).length > 0) {
        const messages = [];
        for (const field in data) {
            const value = data[field];
            const prefix = field === "non_field_errors" ? "" : `${field}: `;
            if (Array.isArray(value)) {
                messages.push(`${prefix}${value.join(", ")}`);
            } else {
                messages.push(`${prefix}${value}`);
            }
        }
        if (messages.length > 0) {
            return messages.join("\n");
        }
    }

    return `Erro ${statusCode}`;
}

function parseList(value) {
    const raw = value.trim();
    if (!raw) {
        return [];
    }

    if (raw.startsWith("[") && raw.endsWith("]")) {
        try {
            const parsed = JSON.parse(raw);
            return Array.isArray(parsed) ? parsed : [parsed];
        } catch {
            return raw.split(",").map(item => item.trim()).filter(Boolean);
        }
    }

    return raw.split(",").map(item => item.trim()).filter(Boolean);
}

function formToJson(form) {
    const data = {};

    for (const element of form.elements) {
        if (!element.name || element.disabled || element.type === "submit" || element.type === "button") {
            continue;
        }

        if (element.type === "checkbox") {
            data[element.name] = element.checked;
            continue;
        }

        if (element.type === "select-multiple") {
            data[element.name] = Array.from(element.options)
                .filter(option => option.selected)
                .map(option => option.value);
            continue;
        }

        if (element.type === "radio") {
            if (element.checked) {
                data[element.name] = element.value;
            }
            continue;
        }

        const value = element.value;
        if (value === "" && element.tagName === "SELECT") {
            data[element.name] = null;
        } else if (["number"].includes(element.type) || ["preco", "valor", "modalidades_inclusas", "duracao_meses", "series", "repeticoes"].includes(element.name)) {
            data[element.name] = value === "" ? null : Number(value);
        } else if (["exercicios", "dias_semana"].includes(element.name)) {
            data[element.name] = parseList(value);
        } else {
            data[element.name] = value;
        }
    }

    if ("aluno_id" in data) {
        data.aluno = data.aluno_id ? Number(data.aluno_id) : null;
        delete data.aluno_id;
    }

    if ("modalidade_id" in data) {
        data.modalidade = data.modalidade_id ? Number(data.modalidade_id) : null;
        delete data.modalidade_id;
    }

    if ("plano" in data) {
        data.plano = data.plano ? Number(data.plano) : null;
    }

    return data;
}

function resolveUserCreateEndpoint(form, data, fallbackUrl) {
    if (form.getAttribute("data-api-user-create") !== "true") {
        return fallbackUrl;
    }

    const perfil = data.perfil || "Aluno";
    const userApiMap = {
        "Administrador": "/api/academia/administradores/",
        "Funcionário": "/api/academia/funcionarios/",
        "FuncionÃ¡rio": "/api/academia/funcionarios/",
        "Aluno": "/api/academia/alunos/",
    };

    delete data.perfil;

    if (perfil === "Administrador") {
        delete data.id_funcionario;
        delete data.cpf;
        delete data.plano;
        delete data.modalidades_inscritas;
    } else if (perfil === "Funcionário" || perfil === "FuncionÃ¡rio") {
        delete data.cpf;
        delete data.plano;
        delete data.modalidades_inscritas;
    } else {
        delete data.id_funcionario;
    }

    return userApiMap[perfil] || fallbackUrl;
}

document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("submit", async function (event) {
        const form = event.target;
        let apiUrl = form.getAttribute("data-api-url");
        if (!apiUrl) {
            return;
        }

        event.preventDefault();

        if (form.getAttribute("data-confirm-delete") === "true" && !window.confirm("Deseja realmente excluir este registro?")) {
            return;
        }

        const method = (form.getAttribute("data-method") || form.method || "POST").toUpperCase();
        const successRedirect = form.getAttribute("data-success-redirect");
        const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]")?.value || getCookie("csrftoken");
        let body = null;

        if (method !== "DELETE") {
            body = formToJson(form);
            apiUrl = resolveUserCreateEndpoint(form, body, apiUrl);
        }

        try {
            if (method === "DELETE") {
                await api.del(apiUrl, csrfToken);
            } else if (method === "PUT") {
                await api.put(apiUrl, body, csrfToken);
            } else if (method === "PATCH") {
                await api.patch(apiUrl, body, csrfToken);
            } else if (method === "POST") {
                await api.post(apiUrl, body, csrfToken);
            } else {
                await request(method, apiUrl, body, csrfToken);
            }

            if (successRedirect) {
                window.location.href = successRedirect;
            } else {
                window.location.reload();
            }
        } catch (error) {
            console.error("API Error:", error);
            alert(error.message || "Erro na requisição. Por favor, tente novamente.");
        }
    });
});
