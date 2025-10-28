#!/usr/bin/env python3
"""
Debug do Sistema de Autenticação
"""

from src.infrastructure.security.auth_manager import auth_manager
import time

def debug_auth():
    print("🔍 Debug do Sistema de Autenticação")
    print("=" * 50)
    
    # 1. Verificar usuário
    user = auth_manager.get_user_by_username('admin')
    print(f"1. Usuário encontrado: {user is not None}")
    if user:
        print(f"   - ID: {user.id}")
        print(f"   - Username: {user.username}")
        print(f"   - Email: {user.email}")
        print(f"   - Role: {user.role}")
        print(f"   - Is Active: {user.is_active}")
        print(f"   - Login Attempts: {user.login_attempts}")
        print(f"   - Locked Until: {user.locked_until}")
        print(f"   - Password Hash: {user.password_hash[:50]}...")
    
    # 2. Verificar senha
    if user:
        password_ok = auth_manager.verify_password('admin123', user.password_hash)
        print(f"2. Senha correta: {password_ok}")
    
    # 3. Testar autenticação passo a passo
    print("\n3. Testando autenticação passo a passo:")
    
    # Verificar se usuário existe
    user = auth_manager.get_user_by_username('admin')
    print(f"   - Usuário existe: {user is not None}")
    
    if not user:
        print("   ❌ Usuário não encontrado")
        return
    
    # Verificar se está bloqueado
    is_locked = user.locked_until and time.time() < user.locked_until
    print(f"   - Está bloqueado: {is_locked}")
    
    if is_locked:
        print("   ❌ Usuário está bloqueado")
        return
    
    # Verificar se está ativo
    print(f"   - Está ativo: {user.is_active}")
    
    if not user.is_active:
        print("   ❌ Usuário está inativo")
        return
    
    # Verificar senha
    password_ok = auth_manager.verify_password('admin123', user.password_hash)
    print(f"   - Senha correta: {password_ok}")
    
    if not password_ok:
        print("   ❌ Senha incorreta")
        return
    
    # Tentar criar token
    try:
        token = auth_manager.create_jwt_token(user)
        print(f"   - Token criado: {token[:50]}...")
        
        # Salvar token
        auth_manager.save_token(token, user.id, "127.0.0.1")
        print("   - Token salvo")
        
        # Resetar tentativas
        auth_manager.reset_login_attempts(user.id)
        print("   - Tentativas resetadas")
        
        # Atualizar último login
        auth_manager.update_last_login(user.id)
        print("   - Último login atualizado")
        
        print(f"\n✅ Autenticação bem-sucedida!")
        print(f"🎫 Token: {token}")
        
    except Exception as e:
        print(f"   ❌ Erro ao criar token: {e}")

if __name__ == "__main__":
    debug_auth()
