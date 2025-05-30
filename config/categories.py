CATEGORIES = {
    'accounting': 'General accounting news and updates',
    'tax': 'Tax law, tax policy, IRS, and tax tech',
    'audit': 'Auditing standards, news, and automation',
    'fintech': 'Financial technology, payments, digital banking',
    'saas': 'Software-as-a-Service industry news',
    'ai': 'Artificial intelligence in accounting/finance',
    'automation': 'Workflow, RPA, and process automation',
    'enterprise': 'Enterprise software, ERP, large org tech',
    'startups': 'Startup launches, funding, and innovation',
    'regulation': 'Compliance, legal, and regulatory news',
    'cybersecurity': 'Security, data privacy, and risk',
    'analytics': 'Data analytics, BI, and reporting',
    'cloud': 'Cloud computing, migration, and services',
    'tech': 'General technology news',
    'practice_mgmt': 'Practice management, firm operations',
    'payroll': 'Payroll tech and news',
    'blockchain': 'Blockchain, crypto, and distributed ledger',
    'cfo_tech': 'CFO technology stack and tools',
    'treasury': 'Treasury management and financial operations',
    'erp': 'Enterprise Resource Planning systems',
    'financial_close': 'Financial close and reporting automation',
    'cash_flow': 'Cash flow management and optimization',
    'expense_mgmt': 'Expense management and spend control'
}

# Keywords associated with each category for content classification
CATEGORY_KEYWORDS = {
    'accounting': ['accounting', 'accountant', 'ledger', 'bookkeeping', 'financial statement', 'balance sheet'],
    'tax': ['tax', 'irs', 'taxation', 'tax law', 'tax policy', 'tax tech', 'tax return'],
    'audit': ['audit', 'auditing', 'auditor', 'internal control', 'assurance'],
    'fintech': ['fintech', 'payments', 'digital banking', 'financial technology', 'open banking'],
    'saas': ['saas', 'software as a service', 'cloud software'],
    'ai': ['ai', 'artificial intelligence', 'machine learning', 'large language model', 'llm'],
    'automation': ['automation', 'rpa', 'robotic process automation', 'workflow automation'],
    'enterprise': ['enterprise', 'erp', 'enterprise resource planning', 'large organization'],
    'startups': ['startup', 'funding', 'venture capital', 'seed round', 'series a', 'series b', 'innovation'],
    'regulation': ['regulation', 'compliance', 'legal', 'regulatory', 'law'],
    'cybersecurity': ['cybersecurity', 'security', 'data privacy', 'risk', 'breach', 'hack'],
    'analytics': ['analytics', 'bi', 'business intelligence', 'reporting', 'data analysis'],
    'cloud': ['cloud', 'cloud computing', 'cloud migration', 'cloud services'],
    'tech': ['tech', 'technology', 'it', 'software', 'hardware'],
    'practice_mgmt': ['practice management', 'firm operations', 'practice mgmt', 'workflow'],
    'payroll': ['payroll', 'payroll tech', 'payroll software'],
    'blockchain': ['blockchain', 'crypto', 'cryptocurrency', 'distributed ledger'],
    'cfo_tech': ['cfo tech', 'cfo technology', 'financial operations', 'finance tech'],
    'treasury': ['treasury', 'treasury management', 'financial operations'],
    'erp': ['erp', 'enterprise resource planning', 'financial operations'],
    'financial_close': ['financial close', 'month-end close', 'accounting close'],
    'cash_flow': ['cash flow', 'working capital', 'financial management'],
    'expense_mgmt': ['expense management', 'spend management', 'cost control']
}

# Companies to track
TRACKED_COMPANIES = {
    'stacks': {
        'name': 'Stacks',
        'url': 'https://stacks.ai/',
        'keywords': ['stacks.ai', 'financial close', 'accounting workflows', 'month-end close']
    },
    'round': {
        'name': 'Round',
        'url': 'https://www.roundtreasury.com/',
        'keywords': ['round treasury', 'treasury management', 'startup capital']
    },
    'light': {
        'name': 'Light',
        'url': 'https://light.inc/',
        'keywords': ['light.inc', 'erp system', 'financial operations']
    },
    'briefcase': {
        'name': 'Briefcase',
        'url': 'https://www.briefcase.so/',
        'keywords': ['briefcase.so', 'accounting automation', 'bookkeeping']
    },
    'mimo': {
        'name': 'Mimo',
        'url': 'https://www.mimohq.com/',
        'keywords': ['mimohq', 'cash flow management', 'accounts payable', 'accounts receivable']
    },
    'bluebook': {
        'name': 'Bluebook',
        'url': 'https://getbluebook.com/',
        'keywords': ['bluebook', 'invoice extraction', 'tax filings']
    },
    'finom': {
        'name': 'Finom',
        'url': 'https://finom.co/',
        'keywords': ['finom', 'financial platform', 'banking services', 'invoicing']
    },
    'abacum': {
        'name': 'Abacum',
        'url': 'https://www.abacum.io/',
        'keywords': ['abacum', 'financial planning', 'budgeting', 'forecasting']
    },
    'payhawk': {
        'name': 'Payhawk',
        'url': 'https://payhawk.com/',
        'keywords': ['payhawk', 'spend management', 'company cards', 'expenses']
    },
    'payflows': {
        'name': 'Payflows',
        'url': 'https://www.payflows.io/',
        'keywords': ['payflows', 'finance operations', 'cfo operations']
    },
    'atlar': {
        'name': 'Atlar',
        'url': 'https://www.atlar.com/',
        'keywords': ['atlar', 'treasury', 'accounting', 'payments']
    },
    'solvimon': {
        'name': 'Solvimon',
        'url': 'https://www.solvimon.com/',
        'keywords': ['solvimon', 'billing', 'monetization', 'pricing models']
    }
} 