<template>
  <div class="textpage-text-wrapper">
    <h3 id="model-intro">Le modèle en bref</h3>
    <strong>Voir la documentation du modèle<a
        href="https://gitlab.inha.fr/snr/rich.data/application/-/blob/final-logilab/db/README.md?ref_type=heads">
        sur le GitLab de l'INHA</a>.</strong>
    <p>La base de données comprend 23 tables. Certaines n&#39;ont pas été remplies car elles correspondent à des
      fonctionnalités ou jeux de données qui n&#39;ont au final pas été implémentées.</p>
    <ul>
      <li>
        <p><strong>Les dates sont en <a
              href="https://www.postgresql.org/docs/current/rangetypes.html"><code>int4range</code></a></strong>
          (tranche
          d&#39;integer, pour représenter des plages d&#39;années). Cela permet de représenter à la fois les dates
          uniques
          (1923) et les tranches de dates (1923-1930).</p>
        <ul>
          <li>les <em>bounds</em> sont <code>[)</code>: début de la tranche inclusive, fin non-inclusive.</li>
          <li><em><code>[1923-1926)</code> = à partir de 1923 inclus et jusqu&#39;à 1926 non-inclus</em>. Pour passer à
            une notation &quot;normale&quot;, on devra donc rétroconvertir en <code>[1923,1925]</code>.</li>
          <li><em><code>[1923-1924)</code> = 1924 (depuis 1923 inclus jusqu&#39;à 1924 non-inclus)</em></li>
          <li>des fonctions existent dans le <em>back</em> et le <em>front</em> pour convertir de
            l&#39;<code>int4range</code> au <code>List[int]</code>.</li>
        </ul>
      </li>
      <li>
        <p><strong>Les géocoordonnées sont stockées dans la base sous la forme de <a
              href="https://en.wikipedia.org/wiki/GeoJSON#Geometries">géométries <code>GeoJSON</code></a></strong> et le
          système de projection utilisé pour toutes les géométries est l&#39;<a
            href="https://epsg.io/4326">EPSG:4326</a>.
        </p>
      </li>
    </ul>
    <p>Pour produire la description des tables ci-dessous, on utilise la requête <a
        href="./query_extract_model.sql"><code>query_extract_model.sql</code></a>, qui produit un tableur. On complète
      ensuite le tableur avant de le transformer en liste à grands coups de regex.</p>
    <hr>
  </div>

  <div class="textpage-text-wrapper">
    <h3 id="model-tables">Description des tables</h3>
    <h4 id="actor">actor</h4>
    <p><code>actor</code> décrit les personnes et entités qui ont produit une ressource iconographique (auteur, autrice
      ou
      maison d’édition)</p>
    <ul>
      <li><strong><code>actor.entry_name</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: le nom de la personne ou entité</li>
        </ul>
      </li>
      <li><strong><code>actor.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>actor.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
    </ul>
    <h4 id="address">address</h4>
    <p>la table <code>address</code> décrit les adresses associées à un lieu</p>
    <ul>
      <li><strong><code>address.address</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: l’adresse en elle-même (nom et numéro de rue)</li>
        </ul>
      </li>
      <li><strong><code>address.city</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: ville</li>
        </ul>
      </li>
      <li><strong><code>address.country</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: pays</li>
        </ul>
      </li>
      <li><strong><code>address.date</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>int4range</code></li>
          <li><strong>description</strong>: tranche de date sur lesquelles cette addresse est identifiée</li>
        </ul>
      </li>
      <li><strong><code>address.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>address.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
      <li><strong><code>address.source</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: texte identifiant la source historique sur laquelle cette adresse est
            identifiée</li>
        </ul>
      </li>
    </ul>
    <h4 id="admin_person">admin_person</h4>
    <p><code>admin_person</code> recense les membres du projet et permet de suivre qui a édité quelle ressource (dans
      les
      faits, ces attributions ont été faites en « batch » : les crédits sont les mêmes pour toutes les ressources
      iconographiques</p>
    <ul>
      <li><strong><code>admin_person.first_name</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: prénom de la personne</li>
        </ul>
      </li>
      <li><strong><code>admin_person.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>admin_person.id_persistent</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant pérenne de la personne : soit un ORCID ou équivalent, soit, si
            rien n’est fourni, un UUID.</li>
        </ul>
      </li>
      <li><strong><code>admin_person.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
      <li><strong><code>admin_person.last_name</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: nom de famille de la personne</li>
        </ul>
      </li>
    </ul>
    <h4 id="annotation">annotation</h4>
    <p><code>annotation</code> permet de stocker des annotations IIIF à ajouter à des documents. à ce state du projet,
      cette table est vide</p>
    <ul>
      <li><strong><code>annotation.content</code></strong> : contenu de l&#39;annotation<ul>
          <li><strong>type PostgreSQL</strong>: json<ul>
              <li><strong>champ nullable</strong>: YES</li>
              <li><strong>description</strong>: contenu de l’annotation, suivant la spécification IIIF pour les
                annotations</li>
            </ul>
          </li>
        </ul>
      </li>
      <li><strong><code>annotation.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>annotation.id_iconography</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>iconography.id</code> : identifiant de la ressource iconographique sur
            laquelle porte cette annotation</li>
        </ul>
      </li>
      <li><strong><code>annotation.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
    </ul>
    <h4 id="cartography">cartography</h4>
    <p><code>cartography</code> contient les métadonnées des ressource cartographiques. Une ressource cartographique
      correspond à une géométrie correspondant à une parcelle issue d’une source historique précise</p>
    <ul>
      <li><strong><code>cartography.crs_epsg</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: le code EPSG du système de projection utilisé pour la géométrie de la
            parcelle
          </li>
        </ul>
      </li>
      <li><strong><code>cartography.date</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>int4range</code></li>
          <li><strong>description</strong>: la plage de dates sur laquelle cette parcelle existe</li>
        </ul>
      </li>
      <li><strong><code>cartography.date_source</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: la date dans le document source</li>
        </ul>
      </li>
      <li><strong><code>cartography.granularity</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: le niveau de granularité de cette parcelle (parcelle, galerie, aile…)</li>
        </ul>
      </li>
      <li><strong><code>cartography.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>cartography.id_licence</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: une valeur de <code>licence.id</code></li>
        </ul>
      </li>
      <li><strong><code>cartography.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
      <li><strong><code>cartography.inventory_number</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: le numéro d’inventaire de la source historique dans l’institution de
            conservation</li>
        </ul>
      </li>
      <li><strong><code>cartography.map_source</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: texte identifiant la source historique à partir de laquelle cette ressource
            est produite</li>
        </ul>
      </li>
      <li><strong><code>cartography.source_url</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: URL vers la page présentant la source sur le site de l’institution de
            conservation</li>
        </ul>
      </li>
      <li><strong><code>cartography.title</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: titre donné à la ressource (souvent un titre générique)</li>
        </ul>
      </li>
      <li><strong><code>cartography.vector</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>json</code></li>
          <li><strong>description</strong>: géométrie de la ressource, au format de Geometry GeoJSON</li>
        </ul>
      </li>
    </ul>
    <h4 id="directory">directory</h4>
    <p><code>directory</code> décrit les entrées de bottins et annuaires océrisés durant la première phase du projet.
      Dans
      les faits, du fait du volume de données et d’erreurs d’OCR, cette table est vide mais peut en théorie accueillir
      toutes les entrées d’annuaires OCRisés, avec une entrée par ligne de la table. La structure de donnée correspond à
      celle produite par Ravinitesh Anapureddy (EPFL)</p>
    <ul>
      <li><strong><code>directory.date</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>int4range</code></li>
          <li><strong>description</strong>: la date de l’entrée d’annuaire</li>
        </ul>
      </li>
      <li><strong><code>directory.entry_name</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: le nom indiqué sur l’annuaire</li>
        </ul>
      </li>
      <li><strong><code>directory.gallica_ark</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: ARK sur gallica BNF de l’annuaire</li>
        </ul>
      </li>
      <li><strong><code>directory.gallica_page</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: page de l’annuaire sur Gallica</li>
        </ul>
      </li>
      <li><strong><code>directory.gallica_row</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: ligne sur laquelle se trouve l’entrée</li>
        </ul>
      </li>
      <li><strong><code>directory.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>directory.id_address</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: une valeur de <code>address.id</code>, permettant de pointer vers l’addresse
            à
            laquelle est liée l’entrée</li>
        </ul>
      </li>
      <li><strong><code>directory.id_licence</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>licence.id</code></li>
        </ul>
      </li>
      <li><strong><code>directory.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
      <li><strong><code>directory.occupation</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: occupation de la personne dans l’annuaire</li>
        </ul>
      </li>
      <li><strong><code>directory.tags</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>ARRAY</code></li>
          <li><strong>description</strong>: liste de tags normalisés pour cette entrée</li>
        </ul>
      </li>
    </ul>
    <h4 id="filename">filename</h4>
    <p><code>filename</code> stocke les noms de fichiers associés aux ressources des tables <code>iconography</code> et
      <code>cartography</code>. Une entrée de <code>filename</code> peut être liée à une ressource iconographique OU
      cartographique
    </p>
    <ul>
      <li><strong><code>filename.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>filename.id_cartography</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: une valeur de <code>cartography.id</code> : identifiant de la ressource
            cartographique à laquelle est liée cette image</li>
        </ul>
      </li>
      <li><strong><code>filename.id_iconography</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: une valeur de <code>iconography.id</code> : identifiant de la ressource
            iconographique à laquelle est liée cette image</li>
        </ul>
      </li>
      <li><strong><code>filename.id_licence</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>licence.id</code></li>
        </ul>
      </li>
      <li><strong><code>filename.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
      <li><strong><code>filename.latlngbounds</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>ARRAY</code></li>
          <li><strong>description</strong>: géocoordonnées de la bounding box dans laquelle positionner cette image sur
            une carte</li>
        </ul>
      </li>
      <li><strong><code>filename.url</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: nom du fichier image dans le serveur de l’INHA. Si le nom contient
            <code>_thumbnail</code>, c’est une image en petit format; si <code>_compress</code>, c’est une image en
            format
            moyen avec compression. Sinon, c’est une image en qualité maximale
          </li>
        </ul>
      </li>
    </ul>
    <h4 id="iconography">iconography</h4>
    <p><code>iconography</code> décrit les ressources iconographiques sur le quartier. Une ressource iconographique est
      un
      document, ou une portion de document, qui est produite dans ou représente le quartier. Une ressource
      iconographique
      peut être composée de plusieurs images (recueils) ou d’une seule.</p>
    <ul>
      <li><strong><code>iconography.corpus</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: corpus ou collection à laquelle appartient la ressource</li>
        </ul>
      </li>
      <li><strong><code>iconography.date</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>int4range</code></li>
          <li><strong>description</strong>: tranche de date sur lesquelles cette addresse est identifiée tes de cette
            ressource</li>
        </ul>
      </li>
      <li><strong><code>iconography.date_corr</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: date corrigée par le projet de cette ressource (non-normalisée)</li>
        </ul>
      </li>
      <li><strong><code>iconography.date_source</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: date fournie par l’institution de conservation de la ressource
            (non-normalisée)</li>
        </ul>
      </li>
      <li><strong><code>iconography.description</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: description de la ressource</li>
        </ul>
      </li>
      <li><strong><code>iconography.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>iconography.id_licence</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>licence.id</code></li>
        </ul>
      </li>
      <li><strong><code>iconography.id_richelieu</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant interne utilisé par le projet pendant la phase de constitution
            du
            corpus</li>
        </ul>
      </li>
      <li><strong><code>iconography.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
      <li><strong><code>iconography.iiif_folio</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>ARRAY</code></li>
          <li><strong>description</strong>: array de Integers ; cette colonne permet de filtrer un manifeste IIIF
            contenant seulement quelques images qui nous intéressent en fournissant une liste d’index des images
            pertinentes. Les index sont la position des canvas dans la <code>sequences[0]/canvases</code> du manifeste
            IIIF</li>
        </ul>
      </li>
      <li><strong><code>iconography.iiif_url</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: URL du manifeste IIIF</li>
        </ul>
      </li>
      <li><strong><code>iconography.inscription</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: inscriptions présentes sur le document</li>
        </ul>
      </li>
      <li><strong><code>iconography.inventory_number</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: numéro d’inventaire dans l’institution de conservation</li>
        </ul>
      </li>
      <li><strong><code>iconography.produced</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>boolean</code></li>
          <li><strong>description</strong>: si <code>True</code>, le document a été produit dans le quartier</li>
        </ul>
      </li>
      <li><strong><code>iconography.represents</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>boolean</code></li>
          <li><strong>description</strong>: si <code>True</code>, le document représente le quartier</li>
        </ul>
      </li>
      <li><strong><code>iconography.source_url</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: URL de la ressource sur le site de l’institution de conservation</li>
        </ul>
      </li>
      <li><strong><code>iconography.technique</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>ARRAY</code></li>
          <li><strong>description</strong>: array de Text : liste des techniques utilisées pour produire le document
          </li>
        </ul>
      </li>
    </ul>
    <h4 id="institution">institution</h4>
    <p><code>institution</code> décrit les institutions de conservation chez lesquelles les ressources iconographiques
      et
      cartographiques ont été trouvées</p>
    <ul>
      <li><strong><code>institution.description</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: description en texte libre</li>
        </ul>
      </li>
      <li><strong><code>institution.entry_name</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: nom canonique de l’institution</li>
        </ul>
      </li>
      <li><strong><code>institution.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>institution.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
    </ul>
    <h4 id="licence">licence</h4>
    <p><code>licence</code> décrit les droits d’accès d’une ressource</p>
    <ul>
      <li><strong><code>licence.description</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: description ou URL de la licence</li>
        </ul>
      </li>
      <li><strong><code>licence.entry_name</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: nom canonique</li>
        </ul>
      </li>
      <li><strong><code>licence.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>licence.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
    </ul>
    <h4 id="named_entity">named_entity</h4>
    <p><code>named_entity</code> décrit les entités nommées, des points d’intérêts (personnes, commerces, lieux...)
      identifiés dans des images</p>
    <ul>
      <li><strong><code>named_entity.category</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: catégorie à laquelle appartient cette entité nommée. Une catégorie regroupe
            plusieurs entités nommées</li>
        </ul>
      </li>
      <li><strong><code>named_entity.category_slug</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: la catégorie, avec seulement des caractères valides à utiliser dans les URL
            de
            l’application</li>
        </ul>
      </li>
      <li><strong><code>named_entity.description</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: description de l’entité nommée</li>
        </ul>
      </li>
      <li><strong><code>named_entity.entry_name</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: nom canonique</li>
        </ul>
      </li>
      <li><strong><code>named_entity.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>named_entity.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
    </ul>
    <h4 id="place">place</h4>
    <p><code>place</code> décrit les différents lieux du quartier. Un lieu est défini par son empreinte au sol et la
      durée
      pendant laquelle il existe. Un lieu existe indépendamment des sources historiques. Il peut être représenté par
      plusieurs ressources cartographiques (le 14 rue Vivienne dans l’atlas Vasserot et le parcellaire municipal fin
      XIXe
      siècle).</p>
    <ul>
      <li><strong><code>place.centroid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>json</code></li>
          <li><strong>description</strong>: le centroïde du lieu</li>
        </ul>
      </li>
      <li><strong><code>place.crs_epsg</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: le code EPSG du système de projection utilisé pour la géométrie</li>
        </ul>
      </li>
      <li><strong><code>place.date</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>int4range</code></li>
          <li><strong>description</strong>: la tranche de date sur laquelle ce lieu est identifié</li>
        </ul>
      </li>
      <li><strong><code>place.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>place.id_place_group</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>place_group.id</code></li>
        </ul>
      </li>
      <li><strong><code>place.id_richelieu</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant interne utilisé par le projet pendant la phase de constitution
            du
            corpus</li>
        </ul>
      </li>
      <li><strong><code>place.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
      <li><strong><code>place.vector</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>json</code></li>
          <li><strong>description</strong>: géométrie du lieu, au format de Geometry GeoJSON</li>
        </ul>
      </li>
      <li><strong><code>place.vector_source</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: mot clé indiquant la source historique d’où a été extraite la géométrie</li>
        </ul>
      </li>
    </ul>
    <h4 id="place_group">place_group</h4>
    <p><code>place_group</code> permet de regrouper ensemble plusieurs lieux (les différentes parcelles du Palais-Royal,
      par exemple). Dans les faits, cette table n’est pas utilisée</p>
    <ul>
      <li><strong><code>place_group.description</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: description du groupe</li>
        </ul>
      </li>
      <li><strong><code>place_group.entry_name</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: nom canonique</li>
        </ul>
      </li>
      <li><strong><code>place_group.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>place_group.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
    </ul>
    <h4 id="r_address_place">r_address_place</h4>
    <p><code>r_address_place</code> : relation entre <code>address</code> et <code>place</code></p>
    <ul>
      <li><strong><code>r_address_place.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>r_address_place.id_address</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>address.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_address_place.id_place</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>place.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_address_place.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
    </ul>
    <h4 id="r_admin_person">r_admin_person</h4>
    <p><code>r_admin_person</code> : relation de <code>admin_person</code> à <code>cartography</code>,
      <code>directory</code> et <code>iconography</code>
    </p>
    <ul>
      <li><strong><code>r_admin_person.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>r_admin_person.id_admin_person</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>admin_person.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_admin_person.id_cartography</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>cartography.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_admin_person.id_directory</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>directory.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_admin_person.id_iconography</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>iconography.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_admin_person.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
    </ul>
    <h4 id="r_cartography_place">r_cartography_place</h4>
    <p><code>r_cartography_place</code> : relation entre <code>cartography</code> et <code>place</code></p>
    <ul>
      <li><strong><code>r_cartography_place.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>r_cartography_place.id_cartography</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>cartography.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_cartography_place.id_place</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>place.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_cartography_place.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
    </ul>
    <h4 id="r_iconography_actor">r_iconography_actor</h4>
    <p><code>r_iconography_actor</code> : relation entre <code>iconography</code> et <code>actor</code></p>
    <ul>
      <li><strong><code>r_iconography_actor.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>r_iconography_actor.id_actor</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>actor.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_iconography_actor.id_iconography</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>iconography.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_iconography_actor.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
      <li><strong><code>r_iconography_actor.ismain</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>boolean</code></li>
          <li><strong>description</strong>: Si <code>True</code>, l’<code>actor</code> de la relation est l’auteur
            principal de la ressource iconographique. Sert à hiérarchiser les auteur.ice.s multiples</li>
        </ul>
      </li>
      <li><strong><code>r_iconography_actor.role</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: &quot;rôle de l’<code>actor</code>: « author » ou «
            publisher&quot;&quot;&quot;</li>
        </ul>
      </li>
    </ul>
    <h4 id="r_iconography_named_entity">r_iconography_named_entity</h4>
    <p><code>r_iconography_named_entity</code> : relation entre <code>iconography</code> et <code>named_entity</code>
    </p>
    <ul>
      <li><strong><code>r_iconography_named_entity.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>r_iconography_named_entity.id_iconography</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>iconography.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_iconography_named_entity.id_named_entity</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>named_entity.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_iconography_named_entity.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
    </ul>
    <h4 id="r_iconography_place">r_iconography_place</h4>
    <p><code>r_iconography_place</code> : relation entre <code>iconography</code> et <code>place</code></p>
    <ul>
      <li><strong><code>r_iconography_place.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>r_iconography_place.id_iconography</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>iconography.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_iconography_place.id_place</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>place.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_iconography_place.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
    </ul>
    <h4 id="r_iconography_theme">r_iconography_theme</h4>
    <p><code>r_iconography_theme</code> : relation entre <code>iconography</code> et <code>theme</code></p>
    <ul>
      <li><strong><code>r_iconography_theme.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>r_iconography_theme.id_iconography</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>iconography.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_iconography_theme.id_theme</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>theme.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_iconography_theme.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
    </ul>
    <h4 id="r_institution">r_institution</h4>
    <p><code>r_institution</code> : relation de <code>institution</code> à <code>cartography</code>,
      <code>directory</code> et <code>iconography</code>
    </p>
    <ul>
      <li><strong><code>r_institution.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>r_institution.id_cartography</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>cartography.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_institution.id_directory</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>directory.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_institution.id_iconography</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>iconography.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_institution.id_institution</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>institution.id</code></li>
        </ul>
      </li>
      <li><strong><code>r_institution.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
    </ul>
    <h4 id="theme">theme</h4>
    <p><code>theme</code> : thématique ou concept à laquelle se rapporte une ressource iconographique. Là où une
      <code>named_entity</code> doit être une chose qui existe, le thème est simplement un concept auquel se rattache
      une
      image
    </p>
    <ul>
      <li><strong><code>theme.category</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: catégorie à laquelle appartient ce thème. Une catégorie regroupe plusieurs
            thèmes</li>
        </ul>
      </li>
      <li><strong><code>theme.category_slug</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: la catégorie, avec seulement des caractères valides à utiliser dans les URL
            de
            l’application</li>
        </ul>
      </li>
      <li><strong><code>theme.description</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: description du thème</li>
        </ul>
      </li>
      <li><strong><code>theme.entry_name</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: nom canonique</li>
        </ul>
      </li>
      <li><strong><code>theme.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>theme.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
    </ul>
    <h4 id="title">title</h4>
    <p><code>title</code> : titre d’une ressource iconographique. Une table à part est crée pour permettre d’avoir
      plusieurs titres par document</p>
    <ul>
      <li><strong><code>title.entry_name</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: le titre en lui-même</li>
        </ul>
      </li>
      <li><strong><code>title.id</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: identifiant interne au format <code>\d+</code></li>
        </ul>
      </li>
      <li><strong><code>title.id_iconography</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>integer</code></li>
          <li><strong>description</strong>: <code>iconography.id</code></li>
        </ul>
      </li>
      <li><strong><code>title.id_uuid</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>text</code></li>
          <li><strong>description</strong>: identifiant public au format <code>qr1[a-z0-9]{32}</code></li>
        </ul>
      </li>
      <li><strong><code>title.ismain</code></strong>
        <ul>
          <li><strong>type PostgreSQL</strong>: <code>boolean</code></li>
          <li><strong>description</strong>: si <code>True</code>, le titre est le titre principal de la ressource.</li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted } from "vue";

/****************************************/

const emit = defineEmits(["h2"]);
const subtitle = "Modèle de données";

/****************************************/

onMounted(() => emit("h2", subtitle))
</script>

<style>
h4 {
  text-decoration: underline;
}

code {
  background-color: var(--cs-negative-default-bg);
  color: var(--cs-negative-default);
  font-size: 80%;
}
</style>