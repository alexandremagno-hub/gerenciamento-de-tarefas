from http import HTTPStatus

import factory.fuzzy
import pytest

from fastapi_zero.models import Todo, TodoState


# TESTE DE CRIAÇÃO DE TODO
def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )
    # Verifica retorno completo
    assert response.json() == {
        'id': 1,
        'title': 'Test todo',
        'description': 'Test todo description',
        'state': 'draft',
    }


# FACTORY DE TODO
class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    # Texto aleatório
    title = factory.Faker('text')
    description = factory.Faker('text')
    # Estado aleatório (enum)
    state = factory.fuzzy.FuzzyChoice(TodoState)
    # Usuário padrão
    user_id = 1


# LISTAGEM SIMPLES
@pytest.mark.asyncio
async def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    # Cria 5 tarefas no banco
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    # Requisição GET
    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
    )
    # Verifica quantidade
    assert len(response.json()['todos']) == expected_todos


# PAGINAÇÃO
@pytest.mark.asyncio
async def test_list_todos_pagination_should_return_2_todos(session, user, client, token):
    expected_todos = 2
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )
    # Deve retornar apenas 2
    assert len(response.json()['todos']) == expected_todos


# FILTRO POR TITLE
@pytest.mark.asyncio
async def test_list_todos_filter_title_should_return_5_todos(session, user, client, token):
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(5, user_id=user.id, title='Test todo 1'))
    await session.commit()

    response = client.get(
        '/todos/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


# FILTRO POR STATE
@pytest.mark.asyncio
async def test_list_todos_filter_state_should_return_5_todos(session, user, client, token):
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft))
    await session.commit()

    response = client.get(
        '/todos/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


# FILTRO COMBINADO
@pytest.mark.asyncio
async def test_list_todos_filter_combined_should_return_5_todos(session, user, client, token):
    expected_todos = 5
    # Tarefas que DEVEM aparecer
    session.add_all(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title='Test todo combined',
            description='combined description',
            state=TodoState.done,
        )
    )
    # Tarefas que NÃO devem aparecer
    session.add_all(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='other description',
            state=TodoState.todo,
        )
    )
    await session.commit()

    response = client.get(
        '/todos/?title=Test todo combined&description=combined&state=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


# PATCH ERRO (TODO NÃO EXISTE)
def test_patch_todo_error(client, token):
    response = client.patch(
        '/todos/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


# PATCH SUCESSO
@pytest.mark.asyncio
async def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    await session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'teste!'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste!'


# DELETE SUCESSO
@pytest.mark.asyncio
async def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    await session.commit()

    response = client.delete(f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted successfully.'}


# DELETE ERRO
def test_delete_todo_error(client, token):
    response = client.delete(f'/todos/{10}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}
