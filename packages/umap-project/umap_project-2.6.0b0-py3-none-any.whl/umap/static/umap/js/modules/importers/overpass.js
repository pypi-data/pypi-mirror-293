import { DomUtil } from '../../../vendors/leaflet/leaflet-src.esm.js'
import { uMapAlert as Alert } from '../../components/alerts/alert.js'
import { BaseAjax, SingleMixin } from '../autocomplete.js'
import { translate } from '../i18n.js'

const TEMPLATE = `
  <h3>Overpass</h3>
  <label>
    <span data-help="overpassImporter">${translate('Expression')}</span>
    <input type="text" placeholder="amenity=drinking_water" name="tags" />
  </label>
  <label>
    ${translate('Geometry mode')}
    <select name="out">
      <option value="geom" selected>${translate('Default')}</option>
      <option value="center">${translate('Only geometry centers')}</option>
    </select>
  </label>
  <label id="area"><span>${translate('Search area')}</span></label>
`

class Autocomplete extends SingleMixin(BaseAjax) {
  handleResults(data) {
    return super.handleResults(data.features)
  }

  createResult(item) {
    return super.createResult({
      // Overpass convention to get their id from an osm one.
      value: item.properties.osm_id + 3600000000,
      label: `${item.properties.name}`,
    })
  }
}

export class Importer {
  constructor(map, options) {
    this.map = map
    this.name = options.name || 'Overpass'
    this.baseUrl = options?.url || 'https://overpass-api.de/api/interpreter'
    this.searchUrl =
      options?.searchUrl ||
      'https://photon.komoot.io/api?q={q}&layer=county&layer=city&layer=state'
    this.id = 'overpass'
  }

  async open(importer) {
    let boundary = null
    let boundaryName = null
    const container = DomUtil.create('div')
    container.innerHTML = TEMPLATE
    this.autocomplete = new Autocomplete(container.querySelector('#area'), {
      url: this.searchUrl,
      placeholder: translate(
        'Type area name, or let empty to load data in current map view'
      ),
      on_select: (choice) => {
        boundary = choice.item.value
        boundaryName = choice.item.label
      },
    })
    this.map.help.parse(container)

    const confirm = (form) => {
      if (!form.tags) {
        Alert.error(translate('Expression is empty'))
        return
      }
      let tags = form.tags
      if (!tags.startsWith('[')) tags = `[${tags}]`
      let area = '{south},{west},{north},{east}'
      if (boundary) area = `area:${boundary}`
      const query = `[out:json];nwr${tags}(${area});out ${form.out};`
      importer.url = `${this.baseUrl}?data=${query}`
      if (boundary) importer.layerName = boundaryName
      importer.format = 'osm'
    }

    importer.dialog
      .open({
        template: container,
        className: `${this.id} importer dark`,
        accept: translate('Choose this data'),
        cancel: false
      })
      .then(confirm)
  }
}
