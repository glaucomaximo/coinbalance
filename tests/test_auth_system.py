#!/usr/bin/env python3
"""
Teste Completo do Sistema de Autenticação
==========================================

Script para testar todas as funcionalidades de autenticação implementadas.
"""

import requests
import json
import time

def test_auth_system():
    """Testa o sistema de autenticação completo."""
    base_url = "http://localhost:8001"
    
    print("🔐 Testando Sistema de Autenticação do CoinBalance")
    print("=" * 60)
    
    # 1. Testar Health Check
    print("\n1. 🏥 Testando Health Check...")
    try:
        response = requests.get(f"{base_url}/health/live", timeout=5)
        if response.status_code == 200:
            print("   ✅ Health check OK")
        else:
            print(f"   ❌ Health check falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro no health check: {e}")
        return False
    
    # 2. Inicializar Super Admin
    print("\n2. 👑 Inicializando Super Admin...")
    try:
        response = requests.post(f"{base_url}/api/v1/auth/init-super-admin")
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Super admin inicializado")
            print(f"   📋 Credenciais: {data['credentials']['username']} / {data['credentials']['password']}")
        else:
            print(f"   ❌ Falha ao inicializar super admin: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro ao inicializar super admin: {e}")
        return False
    
    # 3. Testar Login
    print("\n3. 🔑 Testando Login...")
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(
            f"{base_url}/api/v1/auth/login",
            json=login_data
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data['access_token']
            print("   ✅ Login bem-sucedido")
            print(f"   🎫 Token obtido: {token[:50]}...")
        else:
            print(f"   ❌ Login falhou: {response.status_code}")
            print(f"   📄 Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erro no login: {e}")
        return False
    
    # 4. Testar Endpoint Protegido
    print("\n4. 🛡️ Testando Endpoint Protegido...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{base_url}/api/v1/auth/me", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Endpoint protegido acessado com sucesso")
            print(f"   👤 Usuário: {data['username']} ({data['role']})")
            print(f"   🔐 Permissões: {len(data['permissions'])} permissões")
        else:
            print(f"   ❌ Falha ao acessar endpoint protegido: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro ao acessar endpoint protegido: {e}")
        return False
    
    # 5. Testar Listagem de Usuários
    print("\n5. 👥 Testando Listagem de Usuários...")
    try:
        response = requests.get(f"{base_url}/api/v1/auth/users", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Listagem de usuários OK: {len(data)} usuários")
            for user in data:
                print(f"      - {user['username']} ({user['role']})")
        else:
            print(f"   ❌ Falha na listagem: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro na listagem: {e}")
        return False
    
    # 6. Testar Criação de Usuário
    print("\n6. ➕ Testando Criação de Usuário...")
    try:
        import time
        unique_username = f"testuser_{int(time.time())}"
        user_data = {
            "username": unique_username,
            "email": f"{unique_username}@coinbalance.com",
            "password": "test123456",
            "role": "viewer"
        }
        response = requests.post(
            f"{base_url}/api/v1/auth/users",
            json=user_data,
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Usuário criado com sucesso")
            print(f"   👤 ID: {data['user_id']}")
            print(f"   📧 Email: {data['email']}")
        else:
            print(f"   ❌ Falha ao criar usuário: {response.status_code}")
            print(f"   📄 Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erro ao criar usuário: {e}")
        return False
    
    # 7. Testar Logout
    print("\n7. 🚪 Testando Logout...")
    try:
        response = requests.post(f"{base_url}/api/v1/auth/logout", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Logout realizado com sucesso")
        else:
            print(f"   ❌ Falha no logout: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro no logout: {e}")
        return False
    
    # 8. Testar Token Revogado
    print("\n8. 🔒 Testando Token Revogado...")
    try:
        response = requests.get(f"{base_url}/api/v1/auth/me", headers=headers)
        
        if response.status_code == 401:
            print("   ✅ Token revogado corretamente")
        else:
            print(f"   ❌ Token não foi revogado: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro ao testar token revogado: {e}")
        return False
    
    print("\n🎉 Todos os testes de autenticação passaram!")
    print("✅ Sistema de autenticação funcionando perfeitamente")
    return True

if __name__ == "__main__":
    success = test_auth_system()
    if success:
        print("\n🚀 Sistema pronto para uso!")
    else:
        print("\n❌ Alguns testes falharam")
