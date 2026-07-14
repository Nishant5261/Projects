import random

JOB_ROLES = [
    {
        "id": "software-engineer",
        "name": "Software Engineer",
        "description": "Backend, frontend, or full-stack software development roles",
        "categories": ["Data Structures", "Algorithms", "System Design", "OOP", "Databases", "Behavioral"],
        "questions": [
            {
                "id": "se-ds-1",
                "category": "Data Structures",
                "difficulty": "medium",
                "text": "Explain the difference between an array and a linked list. When would you prefer one over the other?",
                "expectedKeyPoints": [
                    "Arrays have contiguous memory allocation with O(1) random access",
                    "Linked lists have dynamic size with O(1) insertion/deletion at known positions",
                    "Arrays are better for random access and cache performance",
                    "Linked lists are better for frequent insertions/deletions",
                    "Arrays have O(n) insertion in middle; linked lists have O(1) at a known node",
                    "Memory overhead of pointers in linked lists"
                ]
            },
            {
                "id": "se-ds-2",
                "category": "Data Structures",
                "difficulty": "medium",
                "text": "What is a hash table and how does it handle collisions?",
                "expectedKeyPoints": [
                    "Hash table uses a hash function to map keys to array indices",
                    "Average O(1) time for insert, delete, search",
                    "Collision resolution: chaining (linked lists at each bucket)",
                    "Collision resolution: open addressing (linear probing, quadratic probing, double hashing)",
                    "Load factor affects performance; rehashing when load factor is high",
                    "Worst case O(n) when many collisions"
                ]
            },
            {
                "id": "se-ds-3",
                "category": "Data Structures",
                "difficulty": "hard",
                "text": "Explain binary search trees and their time complexity for common operations.",
                "expectedKeyPoints": [
                    "BST: left child < parent < right child",
                    "Average case O(log n) for search, insert, delete",
                    "Worst case O(n) for skewed/unbalanced tree",
                    "In-order traversal gives sorted sequence",
                    "Self-balancing trees (AVL, Red-Black) guarantee O(log n)",
                    "Use cases: sorted data, range queries"
                ]
            },
            {
                "id": "se-ds-4",
                "category": "Data Structures",
                "difficulty": "easy",
                "text": "What is a stack and a queue? Give real-world examples of each.",
                "expectedKeyPoints": [
                    "Stack: LIFO (Last In First Out)",
                    "Queue: FIFO (First In First Out)",
                    "Stack examples: function call stack, undo/redo operations, browser history back button",
                    "Queue examples: task scheduling, print queue, BFS traversal, message queues",
                    "Stack operations: push, pop, peek",
                    "Queue operations: enqueue, dequeue"
                ]
            },
            {
                "id": "se-algo-1",
                "category": "Algorithms",
                "difficulty": "medium",
                "text": "Explain the difference between BFS and DFS. When would you use each?",
                "expectedKeyPoints": [
                    "BFS explores level by level using a queue",
                    "DFS explores depth-first using a stack or recursion",
                    "BFS finds shortest path in unweighted graphs",
                    "DFS is better for detecting cycles, topological sort",
                    "BFS uses more memory (O(w) where w is max width)",
                    "DFS uses O(h) memory where h is max depth"
                ]
            },
            {
                "id": "se-algo-2",
                "category": "Algorithms",
                "difficulty": "hard",
                "text": "What is dynamic programming? Explain with an example.",
                "expectedKeyPoints": [
                    "Breaking problems into overlapping subproblems",
                    "Storing solutions to avoid redundant computation (memoization)",
                    "Bottom-up (tabulation) vs top-down (memoization) approaches",
                    "Optimal substructure property required",
                    "Classic examples: Fibonacci, knapsack, longest common subsequence",
                    "Time-space tradeoff: uses extra memory to save time"
                ]
            },
            {
                "id": "se-algo-3",
                "category": "Algorithms",
                "difficulty": "medium",
                "text": "What is the time and space complexity of merge sort? How does it work?",
                "expectedKeyPoints": [
                    "Time complexity O(n log n) in all cases",
                    "Space complexity O(n) for auxiliary space",
                    "Divide and conquer: split into halves recursively",
                    "Merge step: compare and merge sorted halves",
                    "Stable sorting algorithm",
                    "Good for linked lists and external sorting"
                ]
            },
            {
                "id": "se-sd-1",
                "category": "System Design",
                "difficulty": "hard",
                "text": "How would you design a URL shortening service like bit.ly?",
                "expectedKeyPoints": [
                    "Generate unique short codes (base62 encoding of ID or hash)",
                    "Database schema: short_code to original URL mapping",
                    "Redirect endpoint: 301/302 redirect",
                    "Caching with Redis for hot URLs",
                    "Handle hash collisions",
                    "Rate limiting to prevent abuse",
                    "Scalability: sharding, CDN for redirect"
                ]
            },
            {
                "id": "se-sd-2",
                "category": "System Design",
                "difficulty": "hard",
                "text": "What are microservices? What are their advantages and disadvantages compared to monoliths?",
                "expectedKeyPoints": [
                    "Microservices: independently deployable services with single responsibility",
                    "Advantages: independent scaling, technology flexibility, fault isolation",
                    "Disadvantages: distributed system complexity, network latency, data consistency challenges",
                    "Service communication: REST, gRPC, message queues",
                    "Monolith: simpler for small teams, lower operational overhead",
                    "When to choose: team size, domain complexity, traffic patterns"
                ]
            },
            {
                "id": "se-oop-1",
                "category": "OOP",
                "difficulty": "medium",
                "text": "Explain the four pillars of Object-Oriented Programming.",
                "expectedKeyPoints": [
                    "Encapsulation: bundling data and methods, hiding internal state",
                    "Inheritance: child class inherits properties and methods from parent",
                    "Polymorphism: same interface, different implementations",
                    "Abstraction: hiding implementation details, exposing only necessary features",
                    "Real-world examples for each concept",
                    "Benefits: code reuse, maintainability, extensibility"
                ]
            },
            {
                "id": "se-oop-2",
                "category": "OOP",
                "difficulty": "medium",
                "text": "What is the SOLID principle? Explain each component.",
                "expectedKeyPoints": [
                    "S - Single Responsibility Principle: class has one reason to change",
                    "O - Open/Closed Principle: open for extension, closed for modification",
                    "L - Liskov Substitution Principle: subclasses can replace base classes",
                    "I - Interface Segregation Principle: small specific interfaces over large general ones",
                    "D - Dependency Inversion Principle: depend on abstractions not concretions",
                    "Benefits: maintainable, scalable, testable code"
                ]
            },
            {
                "id": "se-db-1",
                "category": "Databases",
                "difficulty": "medium",
                "text": "What is database indexing and how does it improve query performance?",
                "expectedKeyPoints": [
                    "Index: data structure (B-tree, hash) that speeds up data retrieval",
                    "Without index: full table scan O(n)",
                    "With index: O(log n) for B-tree indexes",
                    "Trade-offs: faster reads, slower writes, additional storage",
                    "Types: primary, secondary, composite, covering indexes",
                    "When NOT to index: small tables, frequently updated columns, low cardinality"
                ]
            },
            {
                "id": "se-db-2",
                "category": "Databases",
                "difficulty": "medium",
                "text": "Explain the difference between SQL and NoSQL databases. When would you choose each?",
                "expectedKeyPoints": [
                    "SQL: relational, structured schema, ACID compliance",
                    "NoSQL: flexible schema, horizontal scaling, eventual consistency",
                    "SQL use cases: complex queries, transactions, structured data",
                    "NoSQL types: document (MongoDB), key-value (Redis), column (Cassandra), graph (Neo4j)",
                    "NoSQL use cases: high write throughput, unstructured data, horizontal scaling",
                    "CAP theorem considerations"
                ]
            },
            {
                "id": "se-beh-1",
                "category": "Behavioral",
                "difficulty": "easy",
                "text": "Tell me about a time you had a conflict with a teammate. How did you resolve it?",
                "expectedKeyPoints": [
                    "Specific situation described (STAR method)",
                    "Listened to the other person's perspective",
                    "Approached conflict professionally and constructively",
                    "Found a common ground or compromise",
                    "Outcome and lessons learned",
                    "Maintained working relationship after resolution"
                ]
            },
            {
                "id": "se-beh-2",
                "category": "Behavioral",
                "difficulty": "easy",
                "text": "Describe a challenging technical problem you solved. What was your approach?",
                "expectedKeyPoints": [
                    "Clear description of the problem and its impact",
                    "Systematic debugging or investigation approach",
                    "Considered multiple solutions before choosing one",
                    "Collaboration with team or research done",
                    "Final solution implemented and its effectiveness",
                    "Lessons learned or process improvements made"
                ]
            },
        ]
    },
    {
        "id": "product-manager",
        "name": "Product Manager",
        "description": "Product strategy, roadmap, and cross-functional leadership roles",
        "categories": ["Product Strategy", "User Research", "Metrics", "Prioritization", "Communication", "Behavioral"],
        "questions": [
            {
                "id": "pm-ps-1",
                "category": "Product Strategy",
                "difficulty": "hard",
                "text": "How would you design a product from scratch for an underserved market segment?",
                "expectedKeyPoints": [
                    "Identify target user and their key pain points through research",
                    "Validate problem with user interviews and surveys",
                    "Define success metrics and north star metric",
                    "Prioritize MVP features vs. nice-to-haves",
                    "Competitive analysis and differentiation strategy",
                    "Go-to-market strategy and launch plan"
                ]
            },
            {
                "id": "pm-ps-2",
                "category": "Product Strategy",
                "difficulty": "medium",
                "text": "How would you decide whether to build, buy, or partner for a new product feature?",
                "expectedKeyPoints": [
                    "Assess strategic importance and core competency",
                    "Evaluate time-to-market requirements",
                    "Cost analysis: development cost vs. acquisition vs. partnership fees",
                    "Risk assessment for each option",
                    "Team capability and bandwidth",
                    "Long-term maintenance and control considerations"
                ]
            },
            {
                "id": "pm-ur-1",
                "category": "User Research",
                "difficulty": "medium",
                "text": "Walk me through how you would conduct user research for a new feature.",
                "expectedKeyPoints": [
                    "Define research objectives and questions",
                    "Choose appropriate methods: interviews, surveys, usability tests",
                    "Recruit representative users (not just power users)",
                    "Conduct sessions without leading questions",
                    "Synthesize findings into patterns and insights",
                    "Translate insights into actionable product decisions"
                ]
            },
            {
                "id": "pm-met-1",
                "category": "Metrics",
                "difficulty": "hard",
                "text": "You notice a 20% drop in user retention. How would you diagnose and address it?",
                "expectedKeyPoints": [
                    "Segment the data by cohort, geography, user type, device",
                    "Look at funnel to identify where drop-off occurs",
                    "Check for recent product changes or external events",
                    "Analyze qualitative feedback and support tickets",
                    "Form hypotheses and prioritize by impact/effort",
                    "Design experiments (A/B tests) to validate solutions"
                ]
            },
            {
                "id": "pm-pri-1",
                "category": "Prioritization",
                "difficulty": "medium",
                "text": "How do you prioritize features when you have conflicting requests from engineering, sales, and users?",
                "expectedKeyPoints": [
                    "Establish clear prioritization framework (RICE, MoSCoW, etc.)",
                    "Align all stakeholders on company goals and OKRs",
                    "Quantify impact: revenue at risk, user impact, strategic value",
                    "Consider engineering effort and technical debt",
                    "Communicate trade-offs transparently to all parties",
                    "Make decision and stand behind it with data"
                ]
            },
            {
                "id": "pm-com-1",
                "category": "Communication",
                "difficulty": "easy",
                "text": "How do you communicate a major product pivot to skeptical stakeholders?",
                "expectedKeyPoints": [
                    "Lead with data and evidence for the pivot",
                    "Acknowledge and address concerns directly",
                    "Explain the opportunity and risk of NOT pivoting",
                    "Outline a clear plan with milestones",
                    "Involve stakeholders in the process",
                    "Set expectations for what success looks like"
                ]
            },
            {
                "id": "pm-beh-1",
                "category": "Behavioral",
                "difficulty": "easy",
                "text": "Tell me about a product decision you made that turned out to be wrong. What did you learn?",
                "expectedKeyPoints": [
                    "Honest acknowledgment of the mistake",
                    "Data or reasoning that led to the wrong decision",
                    "How you detected the decision was wrong",
                    "Actions taken to course correct",
                    "Process improvements made to avoid similar mistakes",
                    "Demonstrates learning mindset and accountability"
                ]
            },
        ]
    },
    {
        "id": "data-scientist",
        "name": "Data Scientist",
        "description": "Machine learning, statistical analysis, and data-driven decision making roles",
        "categories": ["Statistics", "Machine Learning", "Data Engineering", "Communication", "Behavioral"],
        "questions": [
            {
                "id": "ds-stat-1",
                "category": "Statistics",
                "difficulty": "medium",
                "text": "Explain the difference between Type I and Type II errors. How do you balance them?",
                "expectedKeyPoints": [
                    "Type I error (False Positive): rejecting true null hypothesis, alpha level",
                    "Type II error (False Negative): failing to reject false null hypothesis, beta level",
                    "Power of a test = 1 - beta",
                    "Trade-off: lowering alpha increases Type II errors",
                    "Context-dependent: medical testing favors minimizing Type II errors",
                    "Sample size affects both types of errors"
                ]
            },
            {
                "id": "ds-stat-2",
                "category": "Statistics",
                "difficulty": "hard",
                "text": "How would you design an A/B test for a new feature? What statistical considerations are important?",
                "expectedKeyPoints": [
                    "Define hypothesis and success metric clearly",
                    "Calculate required sample size (power analysis)",
                    "Random assignment to control and treatment groups",
                    "Run for sufficient duration to avoid novelty effects",
                    "Check for network effects or spillover",
                    "Multiple testing problem and correction methods (Bonferroni)",
                    "Practical vs. statistical significance"
                ]
            },
            {
                "id": "ds-ml-1",
                "category": "Machine Learning",
                "difficulty": "medium",
                "text": "Explain bias-variance tradeoff and how it affects model selection.",
                "expectedKeyPoints": [
                    "Bias: error from wrong assumptions in the learning algorithm (underfitting)",
                    "Variance: error from sensitivity to fluctuations in training data (overfitting)",
                    "High bias: simple models that miss patterns",
                    "High variance: complex models that memorize training data",
                    "Optimal model minimizes total error (bias² + variance + noise)",
                    "Techniques: regularization, cross-validation, ensemble methods"
                ]
            },
            {
                "id": "ds-ml-2",
                "category": "Machine Learning",
                "difficulty": "hard",
                "text": "How would you handle a heavily imbalanced dataset in a classification problem?",
                "expectedKeyPoints": [
                    "Understand the business context and cost of false positives vs. false negatives",
                    "Use appropriate metrics: F1, AUC-ROC, precision-recall curve instead of accuracy",
                    "Resampling: oversampling minority (SMOTE) or undersampling majority",
                    "Class weight adjustment in model training",
                    "Threshold tuning based on business requirements",
                    "Ensemble methods like balanced random forests"
                ]
            },
            {
                "id": "ds-ml-3",
                "category": "Machine Learning",
                "difficulty": "medium",
                "text": "Explain the difference between supervised, unsupervised, and reinforcement learning.",
                "expectedKeyPoints": [
                    "Supervised: labeled data, predicts output (classification, regression)",
                    "Unsupervised: no labels, finds patterns (clustering, dimensionality reduction)",
                    "Reinforcement: agent learns via rewards/penalties in environment",
                    "Supervised examples: spam detection, image classification",
                    "Unsupervised examples: customer segmentation, anomaly detection",
                    "Reinforcement examples: game playing, robotics, recommendation systems"
                ]
            },
            {
                "id": "ds-de-1",
                "category": "Data Engineering",
                "difficulty": "medium",
                "text": "How would you deal with missing data in a dataset? What are the trade-offs of each approach?",
                "expectedKeyPoints": [
                    "Understand why data is missing: MCAR, MAR, MNAR",
                    "Deletion: listwise or pairwise, loses data but simple",
                    "Mean/median/mode imputation: fast but ignores relationships",
                    "Model-based imputation: k-NN, regression imputation",
                    "Multiple imputation for uncertainty quantification",
                    "Document missingness as a feature (indicator variable)"
                ]
            },
            {
                "id": "ds-com-1",
                "category": "Communication",
                "difficulty": "easy",
                "text": "How do you explain a complex machine learning model's results to non-technical stakeholders?",
                "expectedKeyPoints": [
                    "Lead with business impact, not technical details",
                    "Use analogies and visuals (charts, not equations)",
                    "Focus on what the model does, not how it works internally",
                    "Explain confidence and uncertainty in plain language",
                    "Address 'what should we do differently' question",
                    "Be ready to go deeper if stakeholders are curious"
                ]
            },
            {
                "id": "ds-beh-1",
                "category": "Behavioral",
                "difficulty": "easy",
                "text": "Describe a time your analysis led to an unexpected or counterintuitive finding. How did you handle it?",
                "expectedKeyPoints": [
                    "Validated the finding rigorously before sharing",
                    "Checked data quality and assumptions",
                    "Sought peer review or sanity checks",
                    "Communicated finding clearly with supporting evidence",
                    "Impact on decision-making or business direction",
                    "Remained open to alternative interpretations"
                ]
            },
        ]
    },
    {
        "id": "frontend-engineer",
        "name": "Frontend Engineer",
        "description": "UI development, web performance, and user experience engineering roles",
        "categories": ["JavaScript", "CSS & HTML", "React", "Performance", "Accessibility", "Behavioral"],
        "questions": [
            {
                "id": "fe-js-1",
                "category": "JavaScript",
                "difficulty": "medium",
                "text": "Explain the event loop in JavaScript. How does asynchronous code work?",
                "expectedKeyPoints": [
                    "JavaScript is single-threaded",
                    "Call stack executes synchronous code",
                    "Web APIs handle async operations (setTimeout, fetch)",
                    "Callback/task queue holds callbacks ready to run",
                    "Event loop moves callbacks from queue to stack when stack is empty",
                    "Microtasks (Promises) have higher priority than macrotasks (setTimeout)"
                ]
            },
            {
                "id": "fe-js-2",
                "category": "JavaScript",
                "difficulty": "medium",
                "text": "What is the difference between `let`, `const`, and `var` in JavaScript?",
                "expectedKeyPoints": [
                    "var: function-scoped, hoisted, can be redeclared",
                    "let: block-scoped, not hoisted (temporal dead zone), can be reassigned",
                    "const: block-scoped, must be initialized, cannot be reassigned",
                    "const does not make objects immutable (values inside can change)",
                    "var hoisting causes unexpected behavior",
                    "Prefer const by default, let when reassignment needed, avoid var"
                ]
            },
            {
                "id": "fe-react-1",
                "category": "React",
                "difficulty": "medium",
                "text": "Explain the React component lifecycle and how hooks replicate lifecycle methods.",
                "expectedKeyPoints": [
                    "Class lifecycle: mounting, updating, unmounting phases",
                    "useEffect with empty deps = componentDidMount",
                    "useEffect with deps = componentDidUpdate for those deps",
                    "useEffect cleanup = componentWillUnmount",
                    "useState replaces this.state",
                    "Custom hooks encapsulate reusable stateful logic"
                ]
            },
            {
                "id": "fe-react-2",
                "category": "React",
                "difficulty": "hard",
                "text": "How does React reconciliation work? What is the Virtual DOM?",
                "expectedKeyPoints": [
                    "Virtual DOM is a lightweight JS representation of the real DOM",
                    "React creates a new virtual DOM tree on each render",
                    "Diffing algorithm compares new and old virtual DOM (O(n) heuristic)",
                    "Keys help React identify which list items changed",
                    "Only changed nodes are updated in the real DOM (batching)",
                    "React Fiber enables incremental rendering and prioritization"
                ]
            },
            {
                "id": "fe-perf-1",
                "category": "Performance",
                "difficulty": "hard",
                "text": "How would you optimize a slow-loading web page? Walk me through your approach.",
                "expectedKeyPoints": [
                    "Measure first: use Lighthouse, WebPageTest, Core Web Vitals",
                    "Reduce bundle size: code splitting, tree shaking, lazy loading",
                    "Optimize images: compression, WebP format, responsive images, lazy loading",
                    "Minimize render-blocking resources",
                    "Use caching: CDN, browser cache, service workers",
                    "Reduce JavaScript execution time"
                ]
            },
            {
                "id": "fe-css-1",
                "category": "CSS & HTML",
                "difficulty": "medium",
                "text": "Explain CSS specificity and how the cascade works.",
                "expectedKeyPoints": [
                    "Specificity hierarchy: inline styles > ID > class/attribute/pseudo-class > element",
                    "Specificity calculated as (a, b, c) tuple",
                    "Cascade: later rules override earlier rules at same specificity",
                    "!important overrides all but should be avoided",
                    "Inherited properties vs. non-inherited properties",
                    "Universal selector (*) has zero specificity"
                ]
            },
            {
                "id": "fe-a11y-1",
                "category": "Accessibility",
                "difficulty": "medium",
                "text": "What is web accessibility and how do you ensure your components are accessible?",
                "expectedKeyPoints": [
                    "WCAG guidelines: perceivable, operable, understandable, robust",
                    "Semantic HTML: use correct elements (button, nav, header, main)",
                    "ARIA roles and labels for custom components",
                    "Keyboard navigation: focus management, tab order",
                    "Sufficient color contrast (4.5:1 for normal text)",
                    "Screen reader testing with NVDA, VoiceOver, or axe tools"
                ]
            },
            {
                "id": "fe-beh-1",
                "category": "Behavioral",
                "difficulty": "easy",
                "text": "Tell me about a time you improved the performance of a frontend application. What was the impact?",
                "expectedKeyPoints": [
                    "Specific application and measurable performance problem",
                    "How you measured and diagnosed the issue",
                    "Technical approach taken to resolve it",
                    "Before and after metrics (load time, bundle size, etc.)",
                    "Challenges encountered during implementation",
                    "Business impact: user retention, conversion, satisfaction"
                ]
            },
        ]
    },
]


def get_role_by_id(role_id: str) -> dict | None:
    for role in JOB_ROLES:
        if role["id"] == role_id:
            return role
    return None


def get_questions_for_session(
    role_id: str,
    difficulty: str,
    count: int,
    categories: list | None = None,
) -> list:
    role = get_role_by_id(role_id)
    if not role:
        return []

    questions = role["questions"]

    if categories:
        questions = [q for q in questions if q["category"] in categories]

    if difficulty == "mixed":
        selected = []
        by_difficulty = {"easy": [], "medium": [], "hard": []}
        for q in questions:
            d = q.get("difficulty", "medium")
            if d in by_difficulty:
                by_difficulty[d].append(q)
        counts = {"easy": max(1, count // 4), "medium": max(1, count // 2), "hard": max(1, count // 4)}
        for d, n in counts.items():
            pool = by_difficulty[d]
            random.shuffle(pool)
            selected.extend(pool[:n])
        remaining = [q for q in questions if q not in selected]
        random.shuffle(remaining)
        selected.extend(remaining[: max(0, count - len(selected))])
        random.shuffle(selected)
        return selected[:count]
    else:
        filtered = [q for q in questions if q.get("difficulty", "medium") == difficulty]
        if len(filtered) < count:
            filtered = questions
        random.shuffle(filtered)
        return filtered[:count]
