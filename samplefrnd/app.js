/* ═══════════════════════════════════════════════
   EUREKA — App Logic: Navigation, Data, API
   ═══════════════════════════════════════════════ */

// ─── STATE ───
const state = { profile: '', curriculum: 'ncert', grade: null, subject: '', chapter: '' };

const PROFILE_LABELS = {
  adhd: '⚡ ADHD', dyslexia: '📖 Dyslexia',
  visual_impairment: '👁️ Visual', hearing_impairment: '🔇 Hearing', cognitive: '🧩 Cognitive'
};

const SUBJECT_ICONS = {
  Mathematics: '📐', Science: '🔬', Physics: '⚛️', Chemistry: '🧪', Biology: '🧬',
  'Social Science': '🌍', English: '📝', Hindi: '🇮🇳', 'Computer Science': '💻',
  default: '📚'
};

// ─── NCERT CURRICULUM DATA ───
const NCERT = {
  1: {
    Mathematics: ['Shapes and Space', 'Numbers from One to Nine', 'Addition', 'Subtraction', 'Numbers from Ten to Twenty', 'Time', 'Measurement', 'Numbers from Twenty-one to Fifty', 'Data Handling', 'Patterns', 'Numbers', 'Money', 'How Many'],
    English: ['A Happy Child', 'Three Little Pigs', 'After a Bath', 'The Bubble the Straw and the Shoe', 'One Little Kitten', 'Lalu and Peelu', 'Once I Saw a Little Bird', 'Mittu and the Yellow Mango', 'Merry-Go-Round', 'Circle', 'If I Were an Apple', 'Our Tree'],
    Hindi: ['झूला', 'आम की कहानी', 'आम की टोकरी', 'पत्ते ही पत्ते', 'पकौड़ी', 'छोटी का कमाल', 'रसोईघर', 'चूहो! म्याऊँ सो रही है', 'बंदर और गिलहरी', 'पगड़ी', 'पतंग', 'गेंद-बल्ला'],
    EVS: ['Me and My Body', 'My Family', 'My School and Neighbourhood', 'Plants Around Us', 'Animals Around Us', 'Food We Eat', 'Water and Weather', 'Seasons', 'Transport', 'Festivals and Celebrations'],
  },
  2: {
    Mathematics: ['What is Long What is Round', 'Counting in Groups', 'How Much Can You Carry', 'Counting in Tens', 'Patterns', 'Footprints', 'Jugs and Mugs', 'Tens and Ones', 'My Funbook', 'Add our Points', 'Lines and Lines', 'Give and Take', 'The Longest Step', 'Birds Come Birds Go', 'How Many Ponytails'],
    English: ['First Day at School', 'Haldi\'s Adventure', 'I am Lucky', 'I Want', 'A Smile', 'The Wind and the Sun', 'Rain', 'Storm in the Garden', 'Funny Bunny', 'Mr. Nobody', 'Curlylocks and the Three Bears', 'On My Blackboard I Can Draw', 'I am the Music Man', 'The Mumbai Musicians'],
    Hindi: ['ऊँट चला', 'भालू ने खेली फुटबॉल', 'म्याऊँ म्याऊँ', 'अधूरा काम', 'दोस्त की मदद', 'बहुत हुआ', 'मेरी किताब', 'तितली और कली', 'बुलबुल', 'मीठी सारंगी', 'टेसू राजा बीच बाज़ार', 'बोलने वाली गुफा', 'सबसे अच्छा पेड़', 'नटखट चूहा', 'एक्की-दोक्की'],
    EVS: ['Our Surroundings', 'Plants and Animals', 'Food', 'Shelter', 'Water', 'Travel', 'People Who Help Us', 'Festivals', 'Earth and Sky', 'Safety Rules'],
  },
  3: {
    Mathematics: ['Where to Look From', 'Fun with Numbers', 'Give and Take', 'Long and Short', 'Shapes and Designs', 'Fun with Give and Take', 'Time Goes On', 'Who is Heavier', 'How Many Times', 'Play with Patterns', 'Jugs and Mugs', 'Can We Share', 'Smart Charts', 'Rupees and Paise'],
    English: ['Good Morning', 'The Magic Garden', 'Bird Talk', 'Nina and the Baby Sparrows', 'Little by Little', 'The Enormous Turnip', 'Sea Song', 'A Little Fish Story', 'Don\'t Tell', 'He is My Brother', 'How Creatures Move', 'The Ship of the Desert', 'Trains'],
    Hindi: ['कक्कू', 'शेखीबाज़ मक्खी', 'चाँद वाली अम्मा', 'मन करता है', 'बहादुर बित्तो', 'हमसे सब कहते', 'टिपटिपवा', 'बंदर बाँट', 'अक्ल बड़ी या भैंस', 'क्योंजीमल और कैसे कैसलिया', 'मीरा बहन और बाघ', 'जब मुझे साँप ने काटा', 'मिर्च का मज़ा', 'सबसे अच्छा पेड़'],
    EVS: ['Poonam\'s Day Out', 'The Plant Fairy', 'Water O Water', 'Our First School', 'Chhotu\'s House', 'Foods We Eat', 'Saying Without Speaking', 'Flying High', 'Its Raining', 'What is Cooking', 'From Here to There', 'Work We Do', 'Sharing Our Feelings', 'The Story of Food'],
  },
  4: {
    Mathematics: ['Building with Bricks', 'Long and Short', 'A Trip to Bhopal', 'Tick-Tick-Tick', 'The Way the World Looks', 'The Junk Seller', 'Jugs and Mugs', 'Carts and Wheels', 'Halves and Quarters', 'Play with Patterns', 'Tables and Shares', 'How Heavy How Light', 'Fields and Fences', 'Smart Charts'],
    English: ['Wake Up', 'Neha\'s Alarm Clock', 'Noses', 'The Little Fir Tree', 'Run', 'Nasruddin\'s Aim', 'Sing a Song of People', 'Going to Buy a Book', 'Don\'t Be Afraid of the Dark', 'Helen Keller', 'The Donkey', 'I had a Little Pony', 'A True Friend', 'Books'],
    Hindi: ['मन के भोले-भाले बादल', 'जैसा सवाल वैसा जवाब', 'किरमिच की गेंद', 'पापा जब बच्चे थे', 'दोस्त की पोशाक', 'नाव बनाओ नाव बनाओ', 'दान का हिसाब', 'कौन', 'स्वतंत्रता की ओर', 'थप्प रोटी थप्प दाल', 'पढ़क्कू की सूझ', 'सुनीता की पहिया कुर्सी', 'हुदहुद', 'मुफ़्त ही मुफ़्त'],
    EVS: ['Going to School', 'Ear to Ear', 'A Day with Nandu', 'The Story of Amrita', 'Anita and the Honeybees', 'Omana\'s Journey', 'From the Window', 'Reaching Grandmother\'s House', 'Changing Families', 'Hu Tu Tu Hu Tu Tu', 'The Valley of Flowers', 'Changing Times', 'A River\'s Tale', 'Basva\'s Farm', 'From Market to Home', 'A Busy Month', 'Nandita in Mumbai', 'Too Much Water Too Little Water', 'Abdul in the Garden', 'Eating Together', 'Food and Fun', 'The World in my Home', 'Pochampalli', 'Home and Abroad'],
  },
  5: {
    Mathematics: ['The Fish Tale', 'Shapes and Angles', 'How Many Squares', 'Parts and Wholes', 'Does it Look the Same', 'Be My Multiple I\'ll be Your Factor', 'Can You See the Pattern', 'Mapping Your Way', 'Boxes and Sketches', 'Tenths and Hundredths', 'Area and its Boundary', 'Smart Charts', 'Ways to Multiply and Divide', 'How Big How Heavy'],
    English: ['Ice-Cream Man', 'Wonderful Waste', 'Teamwork', 'Flying Together', 'My Shadow', 'Robinson Crusoe Discovers a Footprint', 'Crying', 'My Elder Brother', 'The Lazy Frog', 'Rip Van Winkle', 'Class Discussion', 'The Talkative Barber', 'Topsy-Turvy Land', 'Gulliver\'s Travels', 'Nobody\'s Friend', 'The Little Bully', 'Sing a Song of People'],
    Hindi: ['राख की रस्सी', 'फसलों के त्योहार', 'खिलौनेवाला', 'नन्हा फ़नकार', 'जहाँ चाह वहाँ राह', 'चिट्ठी का सफ़र', 'डाकिए की कहानी', 'वे दिन भी क्या दिन थे', 'एक माँ की बेबसी', 'एक दिन की बादशाहत', 'चावल की रोटियाँ', 'गुरु और चेला', 'स्वामी की दादी', 'बड़े-बड़े कारखाने इत्यादि'],
    EVS: ['Super Senses', 'A Snake Charmer\'s Story', 'From Tasting to Digesting', 'Mangoes Round the Year', 'Seeds and Seeds', 'Every Drop Counts', 'Experiments with Water', 'A Treat for Mosquitoes', 'Up You Go', 'Walls Tell Stories', 'Sunita in Space', 'What if it Finishes', 'A Shelter so High', 'When the Earth Shook', 'Blow Hot Blow Cold', 'Who Will Do This Work', 'Across the Wall', 'No Place for Us', 'A Seed Tells a Farmer\'s Story', 'Whose Forests', 'Like Father Like Daughter', 'On the Move Again'],
  },
  6: {
    Mathematics: ['Knowing Our Numbers', 'Whole Numbers', 'Playing with Numbers', 'Basic Geometrical Ideas', 'Understanding Elementary Shapes', 'Integers', 'Fractions', 'Decimals', 'Data Handling', 'Mensuration', 'Algebra', 'Ratio and Proportion', 'Symmetry', 'Practical Geometry'],
    Science: ['Food: Where Does It Come From?', 'Components of Food', 'Fibre to Fabric', 'Sorting Materials into Groups', 'Separation of Substances', 'Changes Around Us', 'Getting to Know Plants', 'Body Movements', 'The Living Organisms', 'Motion and Measurement', 'Light Shadows and Reflections', 'Electricity and Circuits', 'Fun with Magnets', 'Water', 'Air Around Us', 'Garbage In Garbage Out'],
    'Social Science': ['The Earth in the Solar System', 'Globe: Latitudes and Longitudes', 'Motions of the Earth', 'Maps', 'Major Domains of the Earth', 'Major Landforms of the Earth', 'Our Country India', 'India: Climate Vegetation and Wildlife'],
    English: ["Who Did Patrick's Homework?", 'How the Dog Found Himself a New Master', 'Taro\'s Reward', 'An Indian American Woman in Space', 'A Different Kind of School', 'Who I Am', 'Fair Play', 'A Game of Chance', 'Desert Animals', 'The Banyan Tree'],
    Hindi: ['वह चिड़िया जो', 'बचपन', 'नादान दोस्त', 'चाँद से थोड़ी सी गप्पें', 'अक्षरों का महत्व', 'पार नज़र के', 'साथी हाथ बढ़ाना', 'ऐसे–ऐसे', 'टिकट–अलबम', 'झाँसी की रानी'],
  },
  7: {
    Mathematics: ['Integers', 'Fractions and Decimals', 'Data Handling', 'Simple Equations', 'Lines and Angles', 'The Triangle and its Properties', 'Congruence of Triangles', 'Comparing Quantities', 'Rational Numbers', 'Practical Geometry', 'Perimeter and Area', 'Algebraic Expressions', 'Exponents and Powers', 'Symmetry', 'Visualising Solid Shapes'],
    Science: ['Nutrition in Plants', 'Nutrition in Animals', 'Fibre to Fabric', 'Heat', 'Acids Bases and Salts', 'Physical and Chemical Changes', 'Weather Climate and Adaptations', 'Winds Storms and Cyclones', 'Soil', 'Respiration in Organisms', 'Transportation in Animals and Plants', 'Reproduction in Plants', 'Motion and Time', 'Electric Current and its Effects', 'Light', 'Water: A Precious Resource', 'Forests: Our Lifeline', 'Wastewater Story'],
    'Social Science': ['Tracing Changes Through a Thousand Years', 'New Kings and Kingdoms', 'The Delhi Sultans', 'The Mughal Empire', 'Rulers and Buildings', 'Towns Traders and Craftspersons', 'Tribes Nomads and Settled Communities', 'Devotional Paths to the Divine', 'The Making of Regional Cultures', 'Eighteenth Century Political Formations'],
    English: ['Three Questions', 'A Gift of Chappals', 'Gopal and the Hilsa Fish', 'The Ashes That Made Trees Bloom', 'Quality', 'Expert Detectives', 'The Invention of Vita-Wonk', 'Fire: Friend and Foe', 'A Bicycle in Good Repair', 'The Story of Cricket'],
  },
  8: {
    Mathematics: ['Rational Numbers', 'Linear Equations in One Variable', 'Understanding Quadrilaterals', 'Data Handling', 'Squares and Square Roots', 'Cubes and Cube Roots', 'Comparing Quantities', 'Algebraic Expressions and Identities', 'Visualising Solid Shapes', 'Mensuration', 'Exponents and Powers', 'Direct and Inverse Proportions', 'Factorisation', 'Introduction to Graphs', 'Playing with Numbers'],
    Science: ['Crop Production and Management', 'Microorganisms: Friend and Foe', 'Synthetic Fibres and Plastics', 'Materials: Metals and Non-Metals', 'Coal and Petroleum', 'Combustion and Flame', 'Conservation of Plants and Animals', 'Cell Structure and Functions', 'Reproduction in Animals', 'Reaching the Age of Adolescence', 'Force and Pressure', 'Friction', 'Sound', 'Chemical Effects of Electric Current', 'Some Natural Phenomena', 'Light', 'Stars and the Solar System', 'Pollution of Air and Water'],
    'Social Science': ['How When and Where', 'From Trade to Territory', 'Ruling the Countryside', 'Tribals Dikus and the Vision of a Golden Age', 'When People Rebel', 'Weavers Iron Smelters and Factory Owners', 'Civilising the Native Educating the Nation', 'Women Caste and Reform', 'The Making of the National Movement', 'India After Independence'],
    English: ['The Best Christmas Present in the World', 'The Tsunami', 'Glimpses of the Past', 'Bepin Choudhury\'s Lapse of Memory', 'The Summit Within', 'This is Jody\'s Fawn', 'A Visit to Cambridge', 'A Short Monsoon Diary', 'The Great Stone Face'],
  },
  9: {
    Mathematics: ['Number Systems', 'Polynomials', 'Coordinate Geometry', 'Linear Equations in Two Variables', 'Introduction to Euclid\'s Geometry', 'Lines and Angles', 'Triangles', 'Quadrilaterals', 'Areas of Parallelograms and Triangles', 'Circles', 'Constructions', 'Heron\'s Formula', 'Surface Areas and Volumes', 'Statistics', 'Probability'],
    Science: ['Matter in Our Surroundings', 'Is Matter Around Us Pure', 'Atoms and Molecules', 'Structure of the Atom', 'The Fundamental Unit of Life', 'Tissues', 'Diversity in Living Organisms', 'Motion', 'Force and Laws of Motion', 'Gravitation', 'Work and Energy', 'Sound', 'Why Do We Fall Ill', 'Natural Resources', 'Improvement in Food Resources'],
    'Social Science': ['The French Revolution', 'Socialism in Europe and the Russian Revolution', 'Nazism and the Rise of Hitler', 'Forest Society and Colonialism', 'Pastoralists in the Modern World', 'India Size and Location', 'Physical Features of India', 'Drainage', 'Climate', 'Natural Vegetation and Wild Life', 'Population', 'What is Democracy Why Democracy', 'Constitutional Design', 'Electoral Politics', 'Working of Institutions', 'Democratic Rights'],
    English: ['The Fun They Had', 'The Sound of Music', 'The Little Girl', 'A Truly Beautiful Mind', 'The Snake and the Mirror', 'My Childhood', 'Packing', 'Reach for the Top', 'The Bond of Love', 'Kathmandu', 'If I Were You'],
    'Computer Science': ['Introduction to IT', 'Operating Systems', 'Word Processing', 'Spreadsheets', 'Presentations', 'Introduction to HTML', 'Cybersafety'],
  },
  10: {
    Mathematics: ['Real Numbers', 'Polynomials', 'Pair of Linear Equations in Two Variables', 'Quadratic Equations', 'Arithmetic Progressions', 'Triangles', 'Coordinate Geometry', 'Introduction to Trigonometry', 'Some Applications of Trigonometry', 'Circles', 'Constructions', 'Areas Related to Circles', 'Surface Areas and Volumes', 'Statistics', 'Probability'],
    Science: ['Chemical Reactions and Equations', 'Acids Bases and Salts', 'Metals and Non-metals', 'Carbon and its Compounds', 'Periodic Classification of Elements', 'Life Processes', 'Control and Coordination', 'How do Organisms Reproduce', 'Heredity and Evolution', 'Light Reflection and Refraction', 'Human Eye and Colourful World', 'Electricity', 'Magnetic Effects of Electric Current', 'Sources of Energy', 'Our Environment', 'Sustainable Management of Natural Resources'],
    'Social Science': ['The Rise of Nationalism in Europe', 'Nationalism in India', 'The Making of a Global World', 'The Age of Industrialisation', 'Print Culture and the Modern World', 'Resources and Development', 'Forest and Wildlife Resources', 'Water Resources', 'Agriculture', 'Minerals and Energy Resources', 'Manufacturing Industries', 'Lifelines of National Economy', 'Power Sharing', 'Federalism', 'Democracy and Diversity', 'Gender Religion and Caste', 'Popular Struggles and Movements', 'Political Parties', 'Outcomes of Democracy', 'Challenges to Democracy'],
    English: ['A Letter to God', 'Nelson Mandela: Long Walk to Freedom', 'Two Stories about Flying', 'From the Diary of Anne Frank', 'The Hundred Dresses', 'The Sermon at Benares', 'The Proposal', 'A Triumph of Surgery', 'The Thief\'s Story', 'The Midnight Visitor', 'A Question of Trust', 'Footprints without Feet', 'The Making of a Scientist', 'The Necklace', 'The Hack Driver', 'Bholi', 'The Book That Saved the Earth'],
    'Computer Science': ['Data Representation', 'Data Communication', 'Networking', 'Web Technologies', 'SQL Basics', 'Cybersecurity Fundamentals'],
  },
  11: {
    Mathematics: ['Sets', 'Relations and Functions', 'Trigonometric Functions', 'Principle of Mathematical Induction', 'Complex Numbers and Quadratic Equations', 'Linear Inequalities', 'Permutations and Combinations', 'Binomial Theorem', 'Sequences and Series', 'Straight Lines', 'Conic Sections', 'Introduction to Three Dimensional Geometry', 'Limits and Derivatives', 'Mathematical Reasoning', 'Statistics', 'Probability'],
    Physics: ['Physical World', 'Units and Measurements', 'Motion in a Straight Line', 'Motion in a Plane', 'Laws of Motion', 'Work Energy and Power', 'System of Particles and Rotational Motion', 'Gravitation', 'Mechanical Properties of Solids', 'Mechanical Properties of Fluids', 'Thermal Properties of Matter', 'Thermodynamics', 'Kinetic Theory', 'Oscillations', 'Waves'],
    Chemistry: ['Some Basic Concepts of Chemistry', 'Structure of Atom', 'Classification of Elements and Periodicity in Properties', 'Chemical Bonding and Molecular Structure', 'States of Matter', 'Thermodynamics', 'Equilibrium', 'Redox Reactions', 'Hydrogen', 'The s-Block Element', 'The p-Block Elements', 'Organic Chemistry: Basic Principles', 'Hydrocarbons', 'Environmental Chemistry'],
    Biology: ['The Living World', 'Biological Classification', 'Plant Kingdom', 'Animal Kingdom', 'Morphology of Flowering Plants', 'Anatomy of Flowering Plants', 'Structural Organisation in Animals', 'Cell: The Unit of Life', 'Biomolecules', 'Cell Cycle and Cell Division', 'Photosynthesis', 'Respiration in Plants', 'Plant Growth and Development', 'Breathing and Exchange of Gases', 'Body Fluids and Circulation', 'Excretory Products and their Elimination', 'Locomotion and Movement', 'Neural Control and Coordination', 'Chemical Coordination and Integration'],
    'Computer Science': ['Computer Overview', 'Software Concepts', 'Data Representation', 'Microprocessors and Memory', 'Data Communication and Networks', 'Introduction to Python', 'Control Structures', 'Functions', 'String Manipulation', 'Lists Tuples and Dictionaries', 'Introduction to SQL'],
  },
  12: {
    Mathematics: ['Relations and Functions', 'Inverse Trigonometric Functions', 'Matrices', 'Determinants', 'Continuity and Differentiability', 'Application of Derivatives', 'Integrals', 'Application of Integrals', 'Differential Equations', 'Vector Algebra', 'Three Dimensional Geometry', 'Linear Programming', 'Probability'],
    Physics: ['Electric Charges and Fields', 'Electrostatic Potential and Capacitance', 'Current Electricity', 'Moving Charges and Magnetism', 'Magnetism and Matter', 'Electromagnetic Induction', 'Alternating Current', 'Electromagnetic Waves', 'Ray Optics and Optical Instruments', 'Wave Optics', 'Dual Nature of Radiation and Matter', 'Atoms', 'Nuclei', 'Semiconductor Electronics', 'Communication Systems'],
    Chemistry: ['The Solid State', 'Solutions', 'Electrochemistry', 'Chemical Kinetics', 'Surface Chemistry', 'Isolation of Elements', 'The p-Block Elements', 'The d and f Block Elements', 'Coordination Compounds', 'Haloalkanes and Haloarenes', 'Alcohols Phenols and Ethers', 'Aldehydes Ketones and Carboxylic Acids', 'Amines', 'Biomolecules', 'Polymers', 'Chemistry in Everyday Life'],
    Biology: ['Reproduction in Organisms', 'Sexual Reproduction in Flowering Plants', 'Human Reproduction', 'Reproductive Health', 'Principles of Inheritance and Variation', 'Molecular Basis of Inheritance', 'Evolution', 'Human Health and Disease', 'Strategies for Food Enhancement', 'Microbes in Human Welfare', 'Biotechnology: Principles and Processes', 'Biotechnology and its Applications', 'Organisms and Populations', 'Ecosystem', 'Biodiversity and Conservation', 'Environmental Issues'],
    'Computer Science': ['Python Revision Tour', 'Object-Oriented Programming', 'File Handling', 'Exception Handling', 'Stack and Queue', 'Linked List', 'Database Concepts', 'SQL Advanced', 'Networking Concepts', 'Web Development Basics', 'Cybersecurity'],
    'Social Science': ['Population Distribution Density Growth', 'Migration Types Causes and Consequences', 'Human Development', 'Human Settlements', 'Land Resources and Agriculture', 'Water Resources', 'Mineral and Energy Resources', 'Manufacturing Industries', 'Planning and Sustainable Development', 'Transport and Communication', 'International Trade'],
  }
};

// ─── SCREEN MANAGEMENT ───
function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  window.scrollTo(0, 0);
}

function goHome() {
  document.documentElement.removeAttribute('data-profile');
  showScreen('s-home');
}

// ─── HOME: PROFILE CARD ANIMATIONS + MAGNETIC SLIDER ───
document.addEventListener('DOMContentLoaded', () => {
  const perspective = document.getElementById('carousel-perspective');
  const cards = Array.from(document.querySelectorAll('.d-card'));

  // ── Coverflow arc config ──
  const SIDE_X = 310;   // px shift for ±1 neighbours
  const SIDE_ROT = 46;    // rotateY° for ±1 neighbours
  const SIDE_SC = 0.80;  // scale of ±1 neighbours
  const FAR_X = 560;   // px shift for ±2 cards
  const FAR_ROT = 68;    // rotateY° for ±2 cards
  const FAR_SC = 0.58;  // scale of ±2 cards
  const DELAY_MS = 0;    // no hover delay — instant response

  let current = 0;
  let hoverTimer = null;

  // ── Position every card based on offset from active ──
  function applyPositions(centerIdx, fadeIn) {
    cards.forEach((card, i) => {
      const off = i - centerIdx;
      const abs = Math.abs(off);
      const dir = Math.sign(off);
      let tx, ry, sc, op, fi, zi;

      if (off === 0) {
        tx = 0; ry = 0; sc = 1; op = 1; fi = 'none'; zi = 10;
      } else if (abs === 1) {
        tx = dir * SIDE_X; ry = -dir * SIDE_ROT; sc = SIDE_SC; op = 0.62; fi = 'brightness(.65)'; zi = 8;
      } else if (abs === 2) {
        tx = dir * FAR_X; ry = -dir * FAR_ROT; sc = FAR_SC; op = 0.30; fi = 'brightness(.45)'; zi = 6;
      } else {
        tx = dir * 900; ry = -dir * 90; sc = 0.3; op = 0; fi = 'none'; zi = 0;
      }

      card.style.zIndex = zi;
      card.style.transform = `translateX(calc(-50% + ${tx}px)) translateY(-50%) rotateY(${ry}deg) scale(${sc})`;
      if (fadeIn) {
        card.style.opacity = String(op);
        card.style.filter = fi;
      }
      card.classList.toggle('active', off === 0);
    });
  }

  // ── Initial layout (no opacity yet — cards start at 0 from CSS) ──
  applyPositions(0, false);

  // ── Staggered fade-in on page load ──
  cards.forEach((card, i) => {
    const op = i === 0 ? 1 : i === 1 ? 0.62 : i === 2 ? 0.30 : 0;
    const fi = i === 1 ? 'brightness(.65)' : i === 2 ? 'brightness(.45)' : 'none';
    setTimeout(() => {
      card.style.opacity = String(op);
      card.style.filter = fi;
    }, 200 + i * 110);
  });

  // ── Click: bring to center OR select profile if already centered ──
  cards.forEach((card, i) => {
    card.addEventListener('click', () => {
      if (i === current) {
        selectProfile(card.dataset.profile);
      } else {
        clearTimeout(hoverTimer);
        current = i;
        applyPositions(i, true);
      }
    });
  });

  // ── Hover: slide to card after delay ──
  cards.forEach((card, i) => {
    card.addEventListener('mouseenter', () => {
      if (i === current) return;
      clearTimeout(hoverTimer);
      hoverTimer = setTimeout(() => {
        current = i;
        applyPositions(i, true);
      }, DELAY_MS);
    });
    card.addEventListener('mouseleave', () => clearTimeout(hoverTimer));
  });
});

function selectProfile(profile) {
  state.profile = profile;
  document.documentElement.setAttribute('data-profile', profile);
  // Update all profile badges
  const label = PROFILE_LABELS[profile] || 'General';
  ['profile-badge-c', 'profile-badge-g', 'profile-badge-s', 'profile-badge-ch'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = label;
  });
  document.getElementById('crumb-curriculum').textContent = label + ' / Choose Curriculum';
  showScreen('s-curriculum');
}

// ─── CURRICULUM ───
function selectCurriculum(curr) {
  state.curriculum = curr;
  document.getElementById('crumb-grade').textContent = PROFILE_LABELS[state.profile] + ' / NCERT / Choose Grade';
  renderGrades();
  showScreen('s-grade');
}

// ─── GRADE ───
function renderGrades() {
  const grid = document.getElementById('grade-grid');
  const grades = Object.keys(NCERT).map(Number).sort((a, b) => a - b);
  grid.innerHTML = grades.map((g, i) => `
    <div class="grade-card" style="animation-delay:${i * 40}ms" onclick="selectGrade(${g})">
      <div class="grade-num">${g}</div>
      <div class="grade-lbl">Grade</div>
    </div>`).join('');
}

function selectGrade(grade) {
  state.grade = grade;
  document.getElementById('crumb-subject').textContent = `${PROFILE_LABELS[state.profile]} / NCERT / Grade ${grade} / Subject`;
  renderSubjects(grade);
  showScreen('s-subject');
}

// ─── SUBJECTS ───
function renderSubjects(grade) {
  const subjects = Object.keys(NCERT[grade] || {});
  const grid = document.getElementById('subject-grid');
  grid.innerHTML = subjects.map((subj, i) => `
    <div class="subject-card" style="animation-delay:${i * 60}ms" onclick="selectSubject('${subj.replace(/'/g, "\\'")}')">
      <div class="sub-icon">${SUBJECT_ICONS[subj] || SUBJECT_ICONS.default}</div>
      <div class="sub-name">${subj}</div>
      <div class="sub-count">${NCERT[grade][subj].length} chapters</div>
    </div>`).join('');
}

function selectSubject(subject) {
  state.subject = subject;
  const chapters = NCERT[state.grade]?.[subject] || [];
  document.getElementById('crumb-chapter').textContent = `${PROFILE_LABELS[state.profile]} / Grade ${state.grade} / ${subject}`;
  document.getElementById('chapter-subject-title').textContent = subject;
  document.getElementById('chapter-intro').textContent =
    `${chapters.length} chapters for Grade ${state.grade}. Select a chapter to get an AI-adapted explanation tailored for your learning profile.`;

  // Preset the ask input with the first chapter as a hint
  document.getElementById('ask-input').placeholder = `e.g. Explain "${chapters[0]}" simply…`;
  document.getElementById('upload-fab').classList.add('show');

  renderChapters(chapters);
  resetPreview();
  showScreen('s-chapter');
}

// ─── CHAPTERS ───
function renderChapters(chapters) {
  const container = document.getElementById('chapter-items');
  container.innerHTML = chapters.map((ch, i) => `
    <div class="ch-item" data-idx="${i}" onclick="selectChapter(${i}, '${ch.replace(/'/g, "\\'")}')">
      <div class="ch-num">${i + 1}</div>
      <div class="ch-name">${ch}</div>
    </div>`).join('');

  // Staggered slide-in from right
  const items = container.querySelectorAll('.ch-item');
  items.forEach((item, i) => {
    setTimeout(() => item.classList.add('reveal'), i * 55);
  });
}

function selectChapter(idx, name) {
  state.chapter = name;
  // Highlight
  document.querySelectorAll('.ch-item').forEach(el => el.classList.remove('selected'));
  document.querySelector(`.ch-item[data-idx="${idx}"]`)?.classList.add('selected');
  // Prefill ask input
  document.getElementById('ask-input').value = `Explain "${name}" in a way that's easy to understand.`;
  // Auto-fetch preview
  fetchAdaptedPreview(name);
}

// ─── AI PREVIEW ───
function resetPreview() {
  document.getElementById('preview-empty').style.display = 'flex';
  document.getElementById('preview-content').style.display = 'none';
  document.getElementById('preview-panel').classList.remove('has-content');
}

async function fetchAdaptedPreview(chapter) {
  const panel = document.getElementById('preview-panel');
  const empty = document.getElementById('preview-empty');
  const content = document.getElementById('preview-content');
  panel.classList.add('has-content');
  empty.style.display = 'none';
  content.style.display = 'block';
  content.innerHTML = `<div class="preview-title">⚡ AI is preparing your content…</div><div class="loading-dots"><span></span><span></span><span></span></div>`;

  try {
    const res = await fetch('/adapt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: `Explain the chapter "${chapter}" from ${state.subject} Grade ${state.grade}`,
        disability_profile: state.profile || undefined,
        grade: state.grade,
        subject: state.subject,
        chapter
      })
    });
    if (!res.ok) {
      const d = await res.json().catch(() => ({}));
      if (res.status === 404) {
        content.innerHTML = `
          <div class="preview-title">📄 No PDF Indexed Yet</div>
          <p style="color:var(--text2);font-size:.85rem;line-height:1.6">
            No educational content has been indexed for this chapter yet.<br/><br/>
            <strong style="color:var(--text)">How to fix:</strong> Click the <strong style="color:var(--p1)">⬆ Upload PDF</strong> button (bottom right) and upload your ${state.subject} textbook PDF. Then try selecting this chapter again.
          </p>`;
      } else {
        throw new Error(d.detail || res.statusText);
      }
      return;
    }
    const data = await res.json();
    renderPreview(chapter, data);
  } catch (err) {
    content.innerHTML = `<div class="preview-title" style="color:#f05050">⚠️ Error</div><p style="color:var(--text2);font-size:.85rem">${err.message}</p>`;
  }
}

function renderPreview(chapter, data) {
  const content = document.getElementById('preview-content');
  let html = `<div class="preview-title">📖 ${chapter}</div>`;
  if (data.simplified) {
    html += `<div class="preview-section"><div class="preview-section-label">📝 Simplified</div><div class="preview-content">${marked.parse(data.simplified)}</div></div>`;
  }
  if (data.visual_description) {
    html += `<div class="preview-section visual"><div class="preview-section-label">👁️ Visual Description</div><div class="preview-content">${marked.parse(data.visual_description)}</div></div>`;
  }
  if (data.tts_script) {
    html += `<div class="preview-section tts"><div class="preview-section-label">🔊 TTS Script</div><div class="preview-content">${marked.parse(data.tts_script)}</div></div>`;
  }
  if (data.sources?.length) {
    html += `<div style="margin-top:12px;display:flex;flex-wrap:wrap;gap:6px">${data.sources.map(s => `<span style="padding:3px 10px;border-radius:12px;font-size:.68rem;background:rgba(88,166,255,.1);border:1px solid rgba(88,166,255,.2);color:var(--p2)">📄 ${s}</span>`).join('')}</div>`;
  }
  content.innerHTML = html;
}

// ─── MANUAL ASK ───
async function sendAdaptQuery() {
  const query = document.getElementById('ask-input').value.trim();
  if (!query) return;
  const btn = document.getElementById('ask-send');
  btn.disabled = true; btn.textContent = '⏳ Thinking…';
  try {
    const res = await fetch('/adapt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query,
        disability_profile: state.profile || undefined,
        grade: state.grade,
        subject: state.subject,
        chapter: state.chapter || undefined
      })
    });
    if (!res.ok) { const d = await res.json().catch(() => ({})); throw new Error(d.detail || res.statusText); }
    const data = await res.json();
    document.getElementById('preview-panel').classList.add('has-content');
    document.getElementById('preview-empty').style.display = 'none';
    document.getElementById('preview-content').style.display = 'block';
    renderPreview(query, data);
  } catch (err) {
    toast(err.message, 'err');
  } finally {
    btn.disabled = false; btn.textContent = 'Get Adapted Explanation →';
  }
}

// ─── UPLOAD ───
let selectedFile = null;
function openUpload() { document.getElementById('upload-overlay').classList.add('open'); }
function closeUpload() { document.getElementById('upload-overlay').classList.remove('open'); }

document.getElementById('upload-overlay').addEventListener('click', e => { if (e.target === document.getElementById('upload-overlay')) closeUpload(); });

const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');

dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('over'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('over'));
dropZone.addEventListener('drop', e => {
  e.preventDefault(); dropZone.classList.remove('over');
  const f = e.dataTransfer.files[0];
  if (f?.name.endsWith('.pdf')) { selectedFile = f; dropZone.textContent = '✅ ' + f.name; dropZone.classList.add('got-file'); }
});
fileInput.addEventListener('change', () => {
  const f = fileInput.files[0];
  if (f) { selectedFile = f; dropZone.textContent = '✅ ' + f.name; dropZone.classList.add('got-file'); }
});

async function doUpload() {
  if (!selectedFile) { toast('Please pick a PDF first', 'err'); return; }
  const btn = document.getElementById('upload-btn');
  btn.textContent = '⏳ Indexing…'; btn.disabled = true;
  const fd = new FormData();
  fd.append('file', selectedFile);
  const grade = document.getElementById('u-grade').value || state.grade;
  const subject = document.getElementById('u-subject').value || state.subject;
  const chapter = document.getElementById('u-chapter').value || state.chapter;
  if (grade) fd.append('grade', grade);
  if (subject) fd.append('subject', subject);
  if (chapter) fd.append('chapter', chapter);
  try {
    const res = await fetch('/ingest', { method: 'POST', body: fd });
    if (!res.ok) { const d = await res.json().catch(() => ({})); throw new Error(d.detail || res.statusText); }
    const data = await res.json();
    toast(`✅ ${data.filename} indexed (${data.chunks_indexed} chunks)`, 'ok');
    closeUpload();
    selectedFile = null;
    dropZone.textContent = '📁 Click or drag PDF here';
    dropZone.classList.remove('got-file');
    // Re-fetch preview for current chapter if any
    if (state.chapter) fetchAdaptedPreview(state.chapter);
  } catch (err) {
    toast('Upload failed: ' + err.message, 'err');
  } finally {
    btn.textContent = '⬆ Upload & Index'; btn.disabled = false;
  }
}

// ─── TOAST ───
let toastTimer;
function toast(msg, type = '') {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = 'toast show ' + type;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove('show'), 3000);
}
