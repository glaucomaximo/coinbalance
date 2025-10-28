'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Wallet, ArrowRightLeft, Box, TrendingUp, Sparkles, Shield } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              CoinBalance
            </h1>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            <Link href="#features" className="text-gray-600 hover:text-gray-900 transition-colors">
              Recursos
            </Link>
            <Link href="#about" className="text-gray-600 hover:text-gray-900 transition-colors">
              Sobre
            </Link>
            <Link href="/docs" className="text-gray-600 hover:text-gray-900 transition-colors">
              Docs
            </Link>
          </nav>
          <div className="flex items-center gap-2">
            <Link href="/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/dashboard">
              <Button>Dashboard</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-50 text-blue-600 text-sm font-medium mb-8">
          <Sparkles className="w-4 h-4" />
          Blockchain Enterprise v1.0
        </div>
        
        <h2 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 via-purple-600 to-blue-600 bg-clip-text text-transparent leading-tight">
          Blockchain Enterprise
          <br />
          com IA e Web3
        </h2>
        
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
          Plataforma completa de blockchain com inteligência artificial integrada,
          carteiras digitais seguras e recursos Web3 avançados.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/dashboard">
            <Button size="lg" className="text-lg px-8 h-12 w-full sm:w-auto">
              Acessar Dashboard
            </Button>
          </Link>
          <Link href="/docs">
            <Button size="lg" variant="outline" className="text-lg px-8 h-12 w-full sm:w-auto">
              Ver Documentação
            </Button>
          </Link>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-8 max-w-2xl mx-auto mt-16">
          <div>
            <p className="text-3xl font-bold text-gray-900">1000x</p>
            <p className="text-sm text-gray-500">Mais Escalável</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-gray-900">6</p>
            <p className="text-sm text-gray-500">Modelos de IA</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-gray-900">100%</p>
            <p className="text-sm text-gray-500">Seguro</p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="container mx-auto px-4 py-20">
        <div className="text-center mb-12">
          <h3 className="text-3xl font-bold mb-4">Recursos Principais</h3>
          <p className="text-gray-600">Tudo que você precisa em uma única plataforma</p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card className="border-2 hover:border-primary-500 transition-all hover:shadow-xl group">
            <CardHeader>
              <div className="w-14 h-14 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Wallet className="w-7 h-7 text-white" />
              </div>
              <CardTitle className="text-xl">Carteiras Digitais</CardTitle>
              <CardDescription className="text-base">
                Crie e gerencie carteiras com segurança enterprise e criptografia avançada AES-256
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-2 hover:border-primary-500 transition-all hover:shadow-xl group">
            <CardHeader>
              <div className="w-14 h-14 rounded-lg bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <ArrowRightLeft className="w-7 h-7 text-white" />
              </div>
              <CardTitle className="text-xl">Transferências</CardTitle>
              <CardDescription className="text-base">
                Realize transferências rápidas e seguras com confirmação em tempo real
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-2 hover:border-primary-500 transition-all hover:shadow-xl group">
            <CardHeader>
              <div className="w-14 h-14 rounded-lg bg-gradient-to-br from-green-500 to-green-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Box className="w-7 h-7 text-white" />
              </div>
              <CardTitle className="text-xl">Blockchain Native</CardTitle>
              <CardDescription className="text-base">
                Explore blocos e transações em tempo real com proof of work genuíno
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-2 hover:border-primary-500 transition-all hover:shadow-xl group">
            <CardHeader>
              <div className="w-14 h-14 rounded-lg bg-gradient-to-br from-orange-500 to-orange-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <TrendingUp className="w-7 h-7 text-white" />
              </div>
              <CardTitle className="text-xl">IA & Analytics</CardTitle>
              <CardDescription className="text-base">
                Predições e análises com 6 modelos de machine learning especializados
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-2 hover:border-primary-500 transition-all hover:shadow-xl group">
            <CardHeader>
              <div className="w-14 h-14 rounded-lg bg-gradient-to-br from-pink-500 to-pink-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Sparkles className="w-7 h-7 text-white" />
              </div>
              <CardTitle className="text-xl">Web3 Completo</CardTitle>
              <CardDescription className="text-base">
                NFTs, DeFi, DAO e cross-chain bridge integrados nativamente
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-2 hover:border-primary-500 transition-all hover:shadow-xl group">
            <CardHeader>
              <div className="w-14 h-14 rounded-lg bg-gradient-to-br from-red-500 to-red-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Shield className="w-7 h-7 text-white" />
              </div>
              <CardTitle className="text-xl">Segurança Enterprise</CardTitle>
              <CardDescription className="text-base">
                Conformidade LGPD, auditoria completa e monitoramento 24/7
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20">
        <Card className="bg-gradient-to-r from-blue-600 to-purple-600 border-0 text-white">
          <CardHeader className="text-center py-16">
            <CardTitle className="text-4xl mb-4 text-white">
              Pronto para começar?
            </CardTitle>
            <CardDescription className="text-xl text-white/90 mb-8">
              Junte-se à revolução blockchain enterprise
            </CardDescription>
            <Link href="/dashboard">
              <Button 
                size="lg" 
                variant="secondary"
                className="text-lg px-8 h-12 bg-white text-blue-600 hover:bg-gray-100"
              >
                Começar Agora
              </Button>
            </Link>
          </CardHeader>
        </Card>
      </section>

      {/* Footer */}
      <footer className="border-t bg-white/80 backdrop-blur-sm mt-20">
        <div className="container mx-auto px-4 py-12">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h4 className="font-semibold mb-4">CoinBalance</h4>
              <p className="text-sm text-gray-600">
                Plataforma blockchain enterprise com IA e Web3
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Produto</h4>
              <ul className="space-y-2 text-sm text-gray-600">
                <li><Link href="/dashboard" className="hover:text-gray-900">Dashboard</Link></li>
                <li><Link href="/docs" className="hover:text-gray-900">Documentação</Link></li>
                <li><Link href="/api" className="hover:text-gray-900">API</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Empresa</h4>
              <ul className="space-y-2 text-sm text-gray-600">
                <li><Link href="/about" className="hover:text-gray-900">Sobre</Link></li>
                <li><Link href="/blog" className="hover:text-gray-900">Blog</Link></li>
                <li><Link href="/contact" className="hover:text-gray-900">Contato</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-gray-600">
                <li><Link href="/privacy" className="hover:text-gray-900">Privacidade</Link></li>
                <li><Link href="/terms" className="hover:text-gray-900">Termos</Link></li>
                <li><Link href="/security" className="hover:text-gray-900">Segurança</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t pt-8 text-center text-sm text-gray-600">
            <p>© 2025 CoinBalance. Desenvolvido com ❤️ pela equipe CoinBalance.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
